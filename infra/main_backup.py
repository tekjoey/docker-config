#!/usr/bin/python3
import sys, importlib, requests, argparse
from pathlib import Path
#sys.path.append('/docker/infra')
import backup_utils as bu

fail = False

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

def test_backup(args):
  if args.noop:
    exit()

#  testing_paths = [Path("/docker/dozzel/backup.py")]
  testing_paths = [Path("/docker/authentik/backup.py"),Path("/docker/calibre-web/backup.py"),Path("/docker/navidrome/backup.py")]

  bu.log("INFO", "MAIN", "------BEGIN testing------")
  bu.log("INFO", "MAIN", "Beginning backup")
  for script in testing_paths:
      run_backup(script)
  bu.log("INFO", "MAIN", "------END testing------")


def full_backup(args):
  if args.noop:
    exit()
  bu.log("INFO", "MAIN", "Beginning backup")

  for script in Path("/docker").rglob("backup.py"):
    run_backup(script)

  data = f"Backup complete. {'No errors found.' if not fail else 'Errors found.'}"
  bu.log("INFO", "MAIN", data, ntfy=True)

def ct_backup(args):
  bu.log("DEBUG", "MAIN", "Subcommand 'ct' was chosen")
  for ct in args.containers:
    path = Path(f"/docker/{ct}/backup.py")
    run_backup(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='DockerBackup',
                    description='Backs-up my Docker containers',
                    )
    parser.add_argument("--debug", action='store_true', help="enable debugging")
    parser.add_argument("--noop", action="store_true", help="ensure that the main backup function is not called. This is for debugging purposes only")

    subparsers = parser.add_subparsers(help='subcommand help')

    # For running the backup scripts against only a few containers.
    testing_parser = subparsers.add_parser('test', help='test help')
    testing_parser.set_defaults(func=test_backup)

    # For backing up every container
    full_parser = subparsers.add_parser('full', help='full help')
    full_parser.set_defaults(func=full_backup)

    # For backing up select containers
    ct_parser = subparsers.add_parser('ct', help='ct help')
    ct_parser.set_defaults(func=ct_backup)
    ct_parser.add_argument('containers', nargs='+')

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
