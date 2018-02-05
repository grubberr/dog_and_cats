#!/Users/ant/dog_and_cats/env/bin/python3

import sys
import argparse
import datetime
from mongoengine.errors import ValidationError
from models import User, Pet, Dog, Cat, date_format
from utils import get_birthday_or_exit

def main(args):

    if args.subparser == 'add':

        birthday = get_birthday_or_exit(args.birthday)

        try:
            u = User.objects.get(id=args.owner)
        except (User.DoesNotExist, ValidationError):
            print("owner not found id = '%s'" % args.owner)
            sys.exit(1)

        if args.type == 'dog':
            p = Dog(name=args.name, birthday=birthday, owner=u)
            p.save()
            print("Dog created id = '%s'" % p.pk)

        elif args.type == 'cat':
            p = Cat(name=args.name, birthday=birthday, owner=u)
            p.save()
            print("Cat created id = '%s'" % p.pk)

    elif args.subparser == 'del':

        try:
            p = Pet.objects.get(id=args.pk)
        except (Pet.DoesNotExist, ValidationError):
            print("pet not found id = '%s'" % args.pk)
        else:
            p.delete()
            print("pet removed id = '%s'" % p.pk)

    elif args.subparser == 'update':

        try:
            p = Pet.objects.get(id=args.pk)
        except (Pet.DoesNotExist, ValidationError):
            print("pet not found id = '%s'" % args.pk)
        else:

            if args.name:
                p.name = args.name

            if args.birthday:
                p.birthday = get_birthday_or_exit(args.birthday)

            p.save()

            print("pet updated id = '%s'" % p.pk)

    elif args.subparser == 'list':

        if args.pk:

            try:
                p = Pet.objects.get(id=args.pk)
            except (Pet.DoesNotExist, ValidationError):
                print("pet not found id = '%s'" % args.pk)
            else:

                if isinstance(p, Cat):
                    print("Cat")
                elif isinstance(p, Dog):
                    print("Dog")

                print("pk = %s" % p.pk)
                print("name = %s" % p.name)
                print("birthday = %s" % p.birthday.strftime(date_format))
        else:

            for p in Pet.objects:
                if isinstance(p, Cat):
                    print("Cat: ", p)
                elif isinstance(p, Dog):
                    print("Dog: ", p)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='subparser')

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('--type', choices=['cat', 'dog'], required=True)
    parser_add.add_argument('--name', required=True)
    parser_add.add_argument('--birthday', required=True)
    parser_add.add_argument('--owner', required=True)

    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('--pk', required=True)
    parser_update.add_argument('--name')
    parser_update.add_argument('--birthday')

    parser_del = subparsers.add_parser('del')
    parser_del.add_argument('--pk', required=True)

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('--pk')

    args = parser.parse_args()

    if args.subparser is None:
        parser.print_help()
        sys.exit(1)

    main(args)
