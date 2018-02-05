#!/Users/ant/dog_and_cats/env/bin/python3

import sys
import argparse
import datetime
from mongoengine.errors import ValidationError
from models import User, date_format, Pet, Cat, Dog
from utils import get_birthday_or_exit

def main(args):

    if args.subparser == 'add':

        birthday = get_birthday_or_exit(args.birthday)

        u = User(
            first_name=args.first_name,
            last_name=args.last_name,
            birthday=birthday)

        u.save()

        print("user created id = '%s'" % u.pk)

    elif args.subparser == 'del':

        try:
            u = User.objects.get(id=args.pk)
        except (User.DoesNotExist, ValidationError):
            print("user not found id = '%s'" % args.pk)
        else:
            u.delete()
            print("user removed id = '%s'" % u.pk)

    elif args.subparser == 'update':

        try:
            u = User.objects.get(id=args.pk)
        except (User.DoesNotExist, ValidationError):
            print("user not found id = '%s'" % args.pk)
        else:

            if args.first_name:
                u.first_name = args.first_name

            if args.last_name:
                u.last_name = args.last_name

            if args.birthday:
                birthday = get_birthday_or_exit(args.birthday)
                u.birthday = birthday

            u.save()

            print("user updated id = '%s'" % u.pk)

    elif args.subparser == 'list':

        if args.pk:

            try:
                u = User.objects.get(id=args.pk)
            except (User.DoesNotExist, ValidationError):
                print("user not found id = '%s'" % args.pk)
            else:
                print("pk = %s" % u.pk)
                print("first_name = %s" % u.first_name)
                print("last_name = %s" % u.last_name)
                print("birthday = %s" % u.birthday.strftime(date_format))
        else:

            for u in User.objects:
                print(u)

    elif args.subparser == 'list_pets':

        try:
            u = User.objects.get(id=args.pk)
        except (User.DoesNotExist, ValidationError):
            print("user not found id = '%s'" % args.pk)
            sys.exit(1)

        print("User: %s %s has next pets:" % (u.first_name, u.last_name))

        for p in Pet.objects(owner=u):
            if isinstance(p, Cat):
                print("Cat: ", p)
            elif isinstance(p, Dog):
                print("Dog: ", p)

    elif args.subparser == 'top':

        from collections import defaultdict
        TOP = defaultdict(list)

        for p in Pet.objects:
            TOP[p.owner].append(p)

        res = list(TOP.items())
        res.sort(key=lambda x:len(x[1]), reverse=True)

        for (u, pets) in res:
            print("%s %s" % (u.first_name, u.last_name))

            for p in pets:
                print("\t", p.name)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='subparser')

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('--first_name', required=True)
    parser_add.add_argument('--last_name', required=True)
    parser_add.add_argument('--birthday', required=True)

    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('--pk', required=True)
    parser_update.add_argument('--first_name')
    parser_update.add_argument('--last_name')
    parser_update.add_argument('--birthday')

    parser_del = subparsers.add_parser('del')
    parser_del.add_argument('--pk', required=True)

    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('--pk')

    parser_list_pets = subparsers.add_parser('list_pets')
    parser_list_pets.add_argument('--pk', required=True)

    parser_top = subparsers.add_parser('top')

    args = parser.parse_args()

    if args.subparser is None:
        parser.print_help()
        sys.exit(1)

    main(args)
