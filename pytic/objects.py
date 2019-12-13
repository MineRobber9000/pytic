import struct
Blocks = {}

class TICFile:
	""".tic file. Has Blocks."""
	def __init__(self):
		self.blocks = []
	def add_block(self,block):
		"""Adds Block `block`."""
		self.blocks.add(block)
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
	def from_fp(cls,fp):
		"""Creates TICFile from a binary read filepointer."""
		self = cls()
		size = fp.seek(0,2)
		fp.seek(0)
		while (fp.tell()<=size):
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
		header0 = ord(fp.read(1))
		if not header0: return None
		bank, block_type = (header0>>5), (header0 & 0b11111)
		size = struct.unpack("<H",fp.read(2))[0]
		reserved_byte = fp.read(1) # unused byte AFAICT
		values = bytearray(fp.read(size))
		cls = Blocks.get(block_type,self)
		return cls(bank,values)
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

class CodeBlock(Block):
	ID = 5
	def _get_content(self):
		return self.values.decode("ascii")
	def _set_content(self,v):
		self.values = bytearray(v,"ascii")
	content = property(_get_content,_set_content,lambda x: None,Block._get_content.__doc__)

Blocks[5]=CodeBlock
