#!/usr/bin/python3
import sys, importlib, requests, argparse
from pathlib import Path
#sys.path.append('/docker/infra')
import backup_utils as bu

fail = False
noop = False

testing_paths = [Path("/docker/authentik/backup.py"),Path("/docker/calibre-web/backup.py"),Path("/docker/navidrome/backup.py")]

def run_backup(path):
    spec = importlib.util.spec_from_file_location("backup_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        bu.log("DEBUG", "MAIN", f"Beginning {path}")
        module.run()
        bu.log("INFO", "MAIN", f"{path} succeeded")
    except Exception as e:
        bu.log("ERROR", "MAIN", f"{path} failed: {e}")
        fail = True

def main():
    if noop:
        exit()
    bu.log("INFO", "MAIN", "Beginning backup")

    for script in Path("/docker").rglob("backup.py"):
        run_backup(script)

    data = f"Backup complete. {'No errors found.' if not fail else 'Errors found.'}"
    bu.log("INFO", "MAIN", data, ntfy=True)

def testing():
    if noop:
        exit()
    bu.log("INFO", "MAIN", "------BEGIN testing------")
    bu.log("INFO", "MAIN", "Beginning backup")


    for script in pathlist:
        run_backup(script)

    bu.log("INFO", "MAIN", "------END testing------")


def test_backup(args):
  print(f"test was called. args are {args}")

def full_backup(args):
  print(f"full was called. args are {args}")

def ct_backup(args):
  print(f"ct was called. args are {args.container}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='DockerBackup',
                    description='Backs-up my Docker containers',
                    )
    subparsers = parser.add_subparsers(help='subcommand help')

    testing_parser = subparsers.add_parser('test', help='test help')
    testing_parser.set_defaults(func=test_backup)


    full_parser = subparsers.add_parser('full', help='full help')
    full_parser.set_defaults(func=full_backup)


    ct_parser = subparsers.add_parser('ct', help='ct help')
    ct_parser.set_defaults(func=ct_backup)
    ct_parser.add_argument('container')

#    parser.add_argument("-t", "--testing", action='store_true', help="enable testing mode where only a few containers are backed-up")
#    parser.add_argument("--noop", action="store_true", help="ensure that the main backup function is not called. This is for debugging purposes only")
#    parser.add_argument("-c", "--container", action='append', help="backup a specific container. Can be called multiple times to backup multiple containers. The name must be identical to their compose folder name")
#    parser.add_argument('--full', action='store_true', help="not currently used")
#    parser.add_argument("--debug", action='store_true', help="enable debugging")
    args = parser.parse_args()
    args.func(args)

    noop = True
#    print(args)


#    if args['noop']:
#        noop = True
#    if args['debug']:
#            bu.logger.setLevel(bu.logging.DEBUG)
#            bu.log("DEBUG", "MAIN", "Debug enabled")
#    if args['container']:
#        noop = True
#        for ct in args['container']:
#            run_backup(Path(f"/docker/{ct}/backup.py"))
#    else:
#        print('no ct')
        # for ct in args['container']:
        #     print(Path(f"/docker/{ct}/backup.py"))

##TODO: This should be altered so main() takes a list of paths to backup.
## This would simplify things with testing and with the single ct backups

#    if args['testing']:
        #print("testing") 
#        testing()
#    else:
       #print("not testing")
 #       main()
