#!/opt/gensoft/exe/TemplateFlow_pyclient/0.8.0/venv/bin/python3.8

import argparse
import os
import sys

#---- as templateflow.api.TF_LAYOUT.root is set at import time based on default or TEMPLATE_FLOW env var
#     and it is not writable, we have to import template flow with environnement set if we want to be
#     abble to set cache dir from command line option

import pprint 

TOOL_VERSION = '0.1'

def parse_args():
    parser = argparse.ArgumentParser(description='TemplateFlow templates retriever.')

    r_group = parser.add_argument_group('retrieve options')
    r_group.add_argument('-r', '--resolution', 
                        action='store',
                        default='unset',
                        help='Index to an specific spatial resolution of the template, multiple values coma separated may be given')

    r_group.add_argument('-s', '--suffix', 
                        action='store',
                        default='unset',
                        help='BIDS suffix')

    r_group.add_argument('-a', '--atlas', 
                        action='store',
                        default='unset',
                        help='Name of a particular atlas')

    r_group.add_argument('-e', '--extension', 
                        action='store',
                        default='unset',
                        help='file extension')

    r_group.add_argument('-H', '--hemi', 
                        action='store',
                        choices=['R', 'L'],
                        default='unset',
                        help='select Hemisphere')

    r_group.add_argument('-S', '--space', 
                        action='store',
                        default='unset',
                        help='Space template is mapped to')

    r_group.add_argument('-d', '--density', 
                        action='store',
                        default='unset',
                        help='Surface density')
    
    r_group.add_argument('-D', '--desc', 
                        action='store',
                        default='unset',
                        help='Description field')

    r_group.add_argument('-c', '--cohort', 
                        action='store',
                        default='unset',
                        help='Template cohort')

    r_group.add_argument('-L', '--label', 
                        action='store',
                        default='unset',
                        help='Template label')

    i_group = parser.add_argument_group('info environement')
    i_group.add_argument('-l', '--list', 
		    action='store_true',
		    default=False,
		    help='list available local templates')

    i_group.add_argument('-m', '--metadata', 
		    action='store_true',
		    default=False,
		    help='Get full metadata for given template')

    i_group.add_argument('-C', '--citations', 
		    action='store_true',
		    default=False,
		    help='Get template citations')

    i_group.add_argument('-B', '--bibtex-citations', 
		    action='store_true',
		    default=False,
		    help='Get template citation in bibtex-citations')

    m_group = parser.add_argument_group('misc options')
    m_group.add_argument('-o', '--tf-cache', 
		    action='store',
		    default='unset',
		    help='Directory to save templates in. default `${HOME}/.cache/templateflow`')

    m_group.add_argument('-v', '--version', 
		    action='store_true',
		    default=False, 
		    help='Display version of this tools AND TemplateFlow Client version')

    parser.add_argument('args', nargs='*',metavar=('template [template ...]') )
    opts = parser.parse_args(sys.argv[1:])
    args = opts.args
    return opts, args


def version_info():
    import templateflow
    prog = os.path.basename(sys.argv[0])
    print(f'{prog} v{TOOL_VERSION}')
    print(f'Using TemplateFlow Client version {templateflow.__version__}')
    sys.exit(0)

def templates_info():
    import templateflow.api as tf
    templates=tf.templates()
    ident_fmt = '\n'.join(templates)
    print(f"{len(templates)} templates:\n-------------------\n{ident_fmt}")
    sys.exit(0)

def metadata_info(args):    
    import templateflow.api as tf
    pp = pprint.PrettyPrinter(indent=4)
    for tmpl in args:
        infos=tf.get_metadata(tmpl)
        pp.pprint(infos)
    sys.exit(0) 

def citation_info(args, bibtex=True):
    import templateflow.api as tf
#    bibtex_format = True if  opts.bibtex_citations else False
    pp = pprint.PrettyPrinter(indent=4)
    for tmpl in args:
        print(tmpl)
        
        infos=tf.get_citations(tmpl, bibtex=bibtex)
        pp.pprint(infos)
    sys.exit(0) 

def template_retriever(args, options):
    import templateflow
    import templateflow.api as tf

    for tmpl in args:
        try: 
            tmpl = tf.get(tmpl, raise_empty=True, **options) 
            print('\n'.join(map(str, tmpl)))
        except Exception as msg:
            print(tmpl, msg)
    sys.exit(0)


def main():
    
    opts, args = parse_args()

    if opts.version:
        version_info()

    if opts.list:
        templates_info()
        
    if opts.metadata:
        metadata_info(args)

    if opts.citations or opts.bibtex_citations:
        citation_info(args, opts.bibtex_citations)

    if opts.tf_cache != 'unset':
        #---- TemplatFlow cache dir was specified, export it
        print("saving to ---------->", opts.tf_cache)
        print("saving to ---------->", os.path.abspath(opts.tf_cache))
        os.environ['TEMPLATEFLOW_HOME'] = os.path.abspath(opts.tf_cache)
    
    #---- allow multi resolution requirement    
    if ',' in opts.resolution:
        opts.resolution = tuple(opts.resolution.split(','))

    #---- clean unset options and be sure to remove non relevant options 
    #     to not introduce unknown arguments when calling tf.get
    options={k:v for k,v in vars(opts).items() if v != 'unset' and v != False}
    non_options = ['list', 'metadata', 'args', 'tf_cache', 'citations', 'bibtex_citation', 'version']
    for e in non_options:
        options.pop(e, None)

    #---- argument None is acquired as a string, not python None. convert it
    for k,v in options.items():
        if v == 'None': options[k] = None

    template_retriever(args, options)


if __name__ == '__main__':
    main()


