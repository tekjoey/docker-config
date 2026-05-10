#!/usr/bin/python3
import requests, argparse
from pathlib import Path
import backup_utils as bu

fail = False

def run_backup(path):
    spec = importlib.util.spec_from_file_location("backup_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        bu.log("DEBUG", "MAIN", f"Beginning to backup {path}")
        module.run()
        bu.log("INFO", "MAIN", f"{path} succeeded")
    except Exception as e:
        bu.log("ERROR", "MAIN", f"{path} failed: {e}")
        fail = True

def test_backup(args):
  bu.log('DEBUG', 'MAIN', f'Main script envoked in testing mode. args are: {args}')
  if args.noop:
    exit()

  testing_paths = [
	Path("/docker/authentik/backup.py"),
	Path("/docker/calibre-web/backup.py"),
	Path("/docker/navidrome/backup.py")
	]

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
    parser.add_argument("--debug", action='store_true', default=3, help="enable debugging. Convinience version of -vvvvv")
    parser.add_argument("--noop", action="store_true", help="ensure that the main backup function is not called. This is for debugging purposes only")
    parser.add_argument('-v', action='count', dest='loglevel', default=0, help='Set Log vebosity. -v will only log CRITICAL levels. -vvvvv will log DEBUG')

    subparsers = parser.add_subparsers(help='subcommand help', required=True)

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

#    bu.logging.setLevel(args.loglevel)


    if args.noop:
      noop = True
      bu.log('DEBUG', 'MAIN', 'Main script envoked with noop=true')

    if args.loglevel > 5:
      bu.logger.setLevel(10)
    if args.loglevel != 0:
      loglevelnum = (60 - (10*args.loglevel))
      print(args.loglevel, "  ", loglevelnum)
      bu.logger.setLevel(loglevelnum)
      bu.log("DEBUG", 'MAIN', f"Log level set to {bu.logging.getLevelName(loglevelnum)}." )


    args.func(args)
