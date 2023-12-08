#!/usr/bin/python3

import cmd, sys, json
from models import storage, FileStorage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review



class HBNBCommand(cmd.Cmd):
	"""Prompt the user with "(hbnb)" before each command."""
	prompt = "(hbnb) "
	cmds = \
		[
			"BaseModel",
			"User",
			"Place",
			"State",
			"City",
			"Amenity",
			"Review"
		]

	def do_quit(self, arg):
		"""quit
		This cmd quit the console by returning True
		"""
		return True

                        
	def do_EOF(self, arg):                               
		"""EOF
		Exit the command interpreter (Ctrl+D)
		"""
		print()
		return True

	def emptyline(self):
		"""Do nothing on empty line"""
		pass
    
	def do_create(self, arg):
			"""create <class>
			Creates a new instance of <class> and save to the Json file
			"""
			args = arg.split()
			if len(args) == 0:
				print("** class name missing **")
			elif args[0] not in HBNBCommand.cmds:
					print("** class doesn't exist **")
			else:
				obj = eval(args[0])()
				print(obj.id)
				storage.save()
	def do_show(self, arg):
		"""show <class> <instance.id>
		Prints the string representation of an instance based
		on the class name and id.
		e.g: $ show BaseModel 1234-1234-1234.
		"""
		args = self.validate_arg(arg)
		if not isinstance(args, list):
			return
		if len(args) == 1:
			print("** instance id missing **")
			return
		all_objts = storage.all()
		if f"{args[0]}.{args[1]}" not in all_objts:
			print("** no instance found **")
		else:
			print(all_objts[f"{args[0]}.{args[1]}"])
	
	def do_destroy(self, arg):
		"""destroy <class> <instance.id>
		Deletes an instance based on the class name and id
		e.g: $ destroy User 1234-1234-1234
		"""
		args = self.validate_arg(arg)
		if not isinstance(args, list):
			return
		if len(args) == 1:
			print("** instance id missing **")
			return
		all_objts = storage.all()
		if f"{args[0]}.{args[1]}" not in all_objts:
			print("** no instance found **")
		else:
			all_objts.pop(f"{args[0]}.{args[1]}")
			storage.save()

	def do_all(self, arg):
		"""all or all <class>
		Prints all string representation of all instances
		based or not on the class name.
		e.g: $ all			(this prints instances of all classes)
		e.g: $ all User		(this prints instances of all User only)
		"""
		args = arg.split()
		if len(args) == 0:
			print([str(i) for i in storage.all().values()])
		else:
			if args[0] not in HBNBCommand.cmds:
				print("** class doesn't exist **")
			else:
				objects = []
				for i in storage.all().values():
					if args[0] == i.__class__.__name__:
						objects.append(str(i))
				print(objects)
	
	def do_update(self, arg):
		"""Updates an instance based on the class name and id
		  by adding or updating attribute
		"""
		pass

	def default(self, line: str):
		if len(line.split()) == 1:
			cmds_callables_all = [i + ".all()" for i in self.cmds]
			cmds_callables_count = [i + ".count()" for i in self.cmds]
			if line in cmds_callables_all:
				# print(dir(line))
				# input()
				line = line.replace(".all()", "")
				self.do_all(line)
			elif line in cmds_callables_count:
				line = line.replace(".count()", "")
				print(self.count(line))
			else:
				super().default(line)
		else:
			super().default(line)
	
	def count(self, clss):
		return len([i for i in storage.all().values() if i.__class__.__name__ == clss])

	

				


			


	@classmethod
	def validate_arg(cls, arg):
		"""validate the arguments. -1 for missing class,
		 -2 for class not exist and list of args for pass"""
		args = arg.split()
		if len(args) == 0:
			print("** class name missing **")
			return -1
		elif args[0] not in cls.cmds:
				print("** class doesn't exist **")
				return -2
		else:
			return args
		
	



if __name__ == '__main__':
    HBNBCommand().cmdloop()


