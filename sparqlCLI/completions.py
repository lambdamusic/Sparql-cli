#!/usr/bin/python
# -*- coding: utf-8 -*-


SPARQL_ENDPOINTS = [
    'http://dbpedia.org/sparql'
    # @todo add more
]




COMPLETIONS = [
    # ===== basic commands =========
    'SELECT', 'DISTINCT', 'COUNT', 'WHERE', 'LIMIT', "GROUP BY", "ORDER BY" ,
    # insert / delete
    
    # ===== queries =========

    # list of entities defined as classes (even if no instances)
    'SELECT ?class WHERE {?class a owl:Class}',
    # list of classes with instances
    'SELECT DISTINCT ?class WHERE {?a a ?class}',
    # list of entities
    'SELECT ?instance ?class WHERE {?instance a ?class}',
    # list of triples
    'SELECT ?a ?b ?c WHERE {?a ?b ?c}',
    # total number of triples
    "SELECT (COUNT(*) AS ?no) { ?s ?p ?o  }",
    # total number of entities
    "SELECT (COUNT(DISTINCT ?s) AS ?no) { ?s a [] }",
    # total number of DISTINCT resource URIs
    "SELECT (COUNT(DISTINCT ?s ) AS ?no) { { ?s ?p ?o  } UNION { ?o ?p ?s } FILTER(!isBlank(?s) && !isLiteral(?s)) }",
    # total number of DISTINCT classes
    "SELECT (COUNT(DISTINCT ?o) AS ?no) { ?s rdf:type ?o }",
    # total number of DISTINCT predicates
    "SELECT (COUNT(DISTINCT ?p) AS ?no) { ?s ?p ?o }",
    # total number of DISTINCT subject nodes
    "SELECT (COUNT(DISTINCT ?s ) AS ?no) {  ?s ?p ?o }",
    # total number of DISTINCT object nodes
    "SELECT (COUNT(DISTINCT ?o ) AS ?no) {  ?s ?p ?o  filter(!isLiteral(?o)) }",
    # exhaustive list of properties used in the dataset
    "SELECT DISTINCT ?p { ?s ?p ?o }",
    # table: class vs. total number of instances of the class
    "SELECT  ?class (COUNT(?s) AS ?COUNT ) { ?s a ?class } GROUP BY ?class ORDER BY ?COUNT",
    # table: property vs. total number of triples using the property
    "SELECT  ?p (COUNT(?s) AS ?COUNT ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?COUNT",
    # table: property vs. total number of DISTINCT subjects in triples using the property
    "SELECT  ?p (COUNT(DISTINCT ?s ) AS ?COUNT ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?COUNT",
    # table: property vs. total number of DISTINCT objects in triples using the property
    "SELECT  ?p (COUNT(DISTINCT ?o ) AS ?COUNT ) { ?s ?p ?o } GROUP BY ?p ORDER BY ?COUNT",
]