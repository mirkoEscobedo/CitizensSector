import argparse, hashlib, sys
from .core import *

def fingerprint():
    files=list((ROOT/'sprite_lab').glob('*.py'))+list(REFS.rglob('*.png'))+list((ROOT/'presets').glob('*.json'))
    files += [ROOT/'experiment.json']
    for p in (ASSETS/'geometry.json',OUT/'raw/M4-attempt-01.png'):
        if p.exists(): files.append(p)
    return hashlib.sha256(''.join(sha(p) for p in sorted(files)).encode()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description='Private, geometry-controlled ship sprite experiment')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    sub.add_parser('check',help='Run software/data gates without private outputs or a game installation')
    for cmd in ('run','compare','validate','export'):
        p=sub.add_parser(cmd); p.add_argument('--ship',choices=['idris'],default='idris')
        if cmd=='run':
            p.add_argument('--methods',choices=['available','baseline'],default='available')
            p.add_argument('--force',action='store_true',help='Recompute deterministic outputs; never repeats provider billing')
        if cmd=='export': p.add_argument('--candidate',default='A04')
    args=parser.parse_args()
    try:
        if args.command=='check':
            from .validation import software_tests
            print(json.dumps(software_tests(),indent=2)); return
        if args.command=='doctor':
            from .environment import doctor
            print(json.dumps(doctor(),indent=2)); return
        if args.command=='run':
            from .environment import doctor
            from .methods import run_methods,resolution_experiment
            from .exporter import export
            from .validation import validate,meaningful_tests
            from .comparison import compare
            from .evidence import finalize
            doctor()
            if args.methods=='baseline': baseline(); print(OUT/'baseline-contact.png'); return
            key=fingerprint(); cache=OUT/'cache.json'
            required=[OUT/'A04.png',OUT/'A05.png',OUT/'A07.png',OUT/'resolution/M1-4x-bicubic.png']
            if args.force or not cache.exists() or load_json(cache).get('key')!=key or not all(p.exists() for p in required):
                run_methods(); resolution_experiment(); save_json(cache,{'key':fingerprint(),'policy':'deterministic stage cache; provider result reused as immutable raw input'})
            export(); validate(); meaningful_tests(); compare(); finalize(); print(OUT/'report.html')
        elif args.command=='compare':
            from .comparison import compare
            compare(); print(OUT/'report.html')
        elif args.command=='validate':
            from .validation import validate,meaningful_tests
            result=validate(); print(json.dumps({'structural_passes':[r['id'] for r in result if r['structural_pass']], 'tests':meaningful_tests()},indent=2))
        elif args.command=='export':
            from .exporter import export
            print(export(args.candidate))
    except KeyboardInterrupt:
        print('Cancelled; completed PNGs and cached provider outputs retained.',file=sys.stderr); sys.exit(130)
    except (FileNotFoundError,ValueError,KeyError) as exc:
        parser.exit(2,f'Lab error: {exc}\nRun doctor, then run --ship idris --methods available. Check README for missing inputs.\n')

if __name__=='__main__': main()
