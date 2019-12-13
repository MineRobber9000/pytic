import struct
Blocks = {}

class TICFile:
	""".tic file. Has Blocks."""
	def __init__(self):
		self.blocks = []
	def add_block(self,block):
		"""Adds Block `block`."""
		self.blocks.append(block)
	def save_to(self,fp):
		"""Saves TICFile. If `fp` is a file name, it is converted to a file pointer."""
		responsible = False
		if type(fp)==str:
			responsible = True
			fp = open(fp,"wb")
		for block in self.blocks:
			block.save_to(fp)
		if responsible:
			fp.close()
	@classmethod
	def from_file(cls,fn):
		with open(fn,"rb") as f:
			return cls.from_fp(f)
	@classmethod
	def from_fp(cls,fp):
		"""Creates TICFile from a binary read filepointer."""
		self = cls()
		size = fp.seek(0,2)
		fp.seek(0)
		while (fp.tell()<size):
			self.add_block(Block.from_fp(fp))
		return self

class Block:
	ID = 0
	"""A block of info."""
	def __init__(self,bank=0,values=bytearray([])):
		self.bank = bank
		self.values = values
	@property
	def size(self):
		"""Size of values."""
		return len(self.values)

	def _get_content(self):
		"""Helpful representation of values, if applicable."""
		return self.values
	def _set_content(self,v):
		"""Set content."""
		self.values = bytearray(v)
	content = property(_get_content,_set_content,lambda x: None,_get_content.__doc__)

	@classmethod
	def from_fp(self,fp):
		global Blocks
		header0 = fp.read(1)
		if not header0: return None
		header0 = ord(header0)
		bank, block_type = (header0>>5), (header0 & 0b11111)
		size = struct.unpack("<H",fp.read(2))[0]
		reserved_byte = fp.read(1) # unused byte AFAICT
		values = bytearray(fp.read(size))
		cls = Blocks.get(block_type,self)
		ret = cls(bank,values)
		ret.block_id = block_type
		return ret
	def save_to(self,fp):
		"""Saves block to file pointer."""
		# bank and chunk type
		fp.write(bytearray([((self.bank<<5)+(self.__class__.ID))]))
		# chunk size
		fp.write(struct.pack("<H",self.size))
		# write 0 to the unused byte
		fp.write(bytearray([0]))
		# write chunk data
		fp.write(self.values)

class GraphicsBlock(Block):
	def _parse_row(self,offset):
		row = []
		for pixel_byte in self.values[offset:offset+4]:
			row.extend([pixel_byte & 0xF,pixel_byte >> 4])
		return row, offset+4
	def _parse_sprite(self,offset):
		pixels = []
		for i in range(8):
			row, offset = self._parse_row(offset)
			pixels.append(row)
		return pixels, offset
	def _parse_content(self):
		sprites = []
		offset = 0
		while offset<len(self.values):
			sprite, offset = self._parse_sprite(offset)
			sprites.append(sprite)
		return sprites
	def _get_content(self):
		return self._parse_content()
	def _set_content(self,v):
		values = bytearray()
		for sprite in v:
			for row in sprite:
				for i in range(0,len(row),2):
					values.append((row[i+1]<<4) | (row[i]))
		self.values = values
	content = property(_get_content,_set_content,lambda x: None,Block._get_content.__doc__)

class TileBlock(GraphicsBlock):
	ID = 1

class SpriteBlock(GraphicsBlock):
	ID = 2

Blocks[1]=TileBlock
Blocks[2]=SpriteBlock

class CodeBlock(Block):
	ID = 5
	def _get_content(self):
		return self.values.decode("ascii")
	def _set_content(self,v):
		self.values = bytearray(v,"ascii")
	content = property(_get_content,_set_content,lambda x: None,Block._get_content.__doc__)

Blocks[5]=CodeBlock
