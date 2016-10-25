#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Summary

An attempt to build a sparql console using python-prompt toolking


@todo
- export results as html / web
- allow passing an endpoint @done
- add more saved queries @done
    - need to try out the queries  with graphDB first!
- store endpoints? eg via an extra command line
- add meta level cli eg .show or .info etc..
- namespaces and shortened URIs
- add multiline support with key shortcut to run code

"""

from __future__ import unicode_literals
import sys
import pygments
import rdflib
from rdflib.plugins.stores.sparqlstore import SPARQLStore
import click
# http://click.pocoo.org/5/python3/
click.disable_unicode_literals_warning = True

from .loader import RDFLoader
from .completions import *


#http://stackoverflow.com/questions/1714027/version-number-comparison
from distutils.version import StrictVersion
if StrictVersion(pygments.__version__) <= StrictVersion('2.1'):
    print "Pygments version 2.2 minimum required (you have %s)" % pygments.__version__
    sys.exit()


from prompt_toolkit import AbortAction, prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from pygments.lexers.rdf import SparqlLexer
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token






sparql_completer = WordCompleter(COMPLETIONS, ignore_case=True)


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)





def run_loop(db):
    """
    Main application loop
    """
    history = InMemoryHistory()

    while True:
        try:
            text = prompt('> ', lexer=SparqlLexer, completer=sparql_completer,
                          style=DocumentStyle, history=history,
                          # multiline=True,
                          on_abort=AbortAction.RETRY)
        except EOFError:
            break  # Control-D pressed.

        if text:
            click.secho("You said \"" + text + "\" (triples in DB: %d)" % len(db), bg='white', fg='black')

            ## == THE QUERY ====

            res = run_query(text, db)

            print_results(res)

            # SUPPRESS THE FOLLOWING?
            # try:
            #     print_results(res)
            # except:
            #     e = sys.exc_info()[0]
            #     print "--error--->", e

            ## ================




def add_ns(db):
    db.bind("rdf", rdflib.namespace.RDF)
    db.bind("rdfs", rdflib.namespace.RDFS)
    db.bind("owl", rdflib.namespace.OWL)
    db.bind("skos", rdflib.namespace.SKOS)



def print_results(res):

    if res:
        counter = 0
        for row in res:
            counter += 1
            click.secho("%d -----" % counter, fg='green')
            for v in res.vars:
                el1 = click.style("[?%s] " % str(v), fg='red')
                try:
                    el2 = click.style(row[str(v)])  
                except:
                    el2 = click.style("Error: variable <?%s> not bound" % str(v))
                click.echo(el1 + el2)             

            # print " ,".join([unicode(x) for x in row])
    else:
        click.secho("No results", fg='red')



def run_query(q, db):
    """ """
    if len(db):
        try:
            qres = db.query(
                """%s""" % q)
            return qres
        except:
            e = sys.exc_info()[0]
            print "--error--->", e
            return None



def load_file_or_uri(source):
    """wrapper around RDFLoader class"""
    _db = RDFLoader()
    try:       
        db = _db.load(source) 
        add_ns(db)
        return db
    except:
        e = sys.exc_info()[0]
        print "--error--->", e   
        return None 


def load_endpoint(url):
    """ eg "http://dbpedia.org/sparql" """
    try:       
        click.secho("...Connecting to %s" % url, fg="green")
        store = SPARQLStore(url)
        db = rdflib.ConjunctiveGraph(store=store)
        add_ns(db)
        return db
    except:
        e = sys.exc_info()[0]
        print "--error--->", e   
        return None 





CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--load', '-l',  help='Load a uri or local file path into a graph.')
@click.option('--endpoint', '-e',  help='Connect to a sparql endpoint.')
@click.option('--suggest',  '-s', help='Suggest some sparql endpoints.', is_flag=True)
def main(load=None, endpoint=None, suggest=False):
    """main"""
    db = None

    if suggest:
        for x in SPARQL_ENDPOINTS:
            print x
        sys.exit(0)

    if not load or endpoint:
        click.secho("Note: please specify a database to query (-h for more help).", fg='red')
        sys.exit(0)

    if load:
        click.secho("Loading: <%s>." % load, fg='green')
        db = load_file_or_uri(load)
    elif endpoint:
        click.secho("Connecting: <%s>." % endpoint, fg='green')
        db = load_endpoint(endpoint)

    if not db:
        click.secho("Note: could not load the database.", fg='red')
        db = rdflib.Graph()

    run_loop(db)

    print('GoodBye!')





if __name__ == '__main__':
    try:
        # http://stackoverflow.com/questions/32553969/modify-usage-string-on-click-command-line-interface-on-windows
        main(prog_name='sparql-cli')
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e






