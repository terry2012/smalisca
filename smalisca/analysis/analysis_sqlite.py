#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# File:         analysis/analysis_sqlite.py
# Created:      2015-02-01
# Purpose:      Analysis functionalities based on SQLite models
#
# Copyright
# -----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2015 Victor Dorneanu <info AAET dornea DOT nu>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""Implements analysis interface for SQLite"""

from smalisca.analysis.analysis_base import AnalysisBase
from smalisca.modules.module_sql_models import SmaliClass, SmaliMethod
from smalisca.modules.module_sql_models import SmaliProperty
from smalisca.modules.module_sql_models import SmaliCall
from smalisca.core.smalisca_logging import log


def row2dict(row):
    """Converts SQLAlchemy row to dict

    Args:
        row: A SQLAlchemy query result object

    Returns
        dict: Returns the row as dictionary

    """
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


class AnalyzerSQLite(AnalysisBase):
    """Implements the analysis interface for SQLite

    Attributes:
        self.db: The SQLAlchemy DB session
        self.graph: A SmaliscaGraph instance


    """

    def __init__(self, db_session):
        """Class constructor

        Args:
            db_session: A SQLAlchemy DB session instance

        """
        self.db = db_session

    def search_class(self, args={}):
        """Searches for classes

        Args:
            args (dict): Specify a dict containing the search criterias

        Examples:
            d = u{'type': 'class_name', 'pattern': 'test'}
            search_class(d)

        Returns:
            list: List of any results, None otherwise.

        """
        result = None
        query = self.db.query(SmaliClass)

        # Search for class
        if ('type' in args) and ('pattern' in args):

            # Search for class id
            if args['type'] == 'id':
                result = query.filter(
                    SmaliClass.id == int(args['pattern'])
                ).all()

            # Search for class names
            elif args['type'] == 'class_name':
                result = query.filter(
                    SmaliClass.class_name.contains(args['pattern'])
                ).all()

            # Search for class types
            elif args['type'] == 'class_type':
                result = query.filter(
                    SmaliClass.class_type.contains(args['pattern'])
                ).all()

            # Search for class package
            elif args['type'] == 'class_package':
                result = query.filter(
                    SmaliClass.class_package.contains(args['pattern'])
                ).all()

            # Search for path location
            elif args['type'] == 'path':
                result = query.filter(
                    SmaliClass.path.contains(args['pattern'])
                ).all()

            else:
                log.error("Invalid search type: %s" % args['type'])
        else:
            result = query.all()

        return result

    def search_property(self, args={}):
        """Searches for class properties

        Args:
            args (dict): Specify a dict containing the search criterias

        Examples:
            d = u{'type': 'property_type', 'pattern': 'private'}
            search_property(d)

        Returns:
            list: List of any results, None otherwise.

        """
        result = None
        query = self.db.query(SmaliProperty)

        # Search for property
        if ('type' in args) and ('pattern' in args):

            # Search for property id
            if args['type'] == 'id':
                result = query.filter(
                    SmaliProperty.id == int(args['pattern'])
                ).all()

            # Search for property name
            elif args['type'] == 'property_name':
                result = query.filter(
                    SmaliProperty.property_name.contains(args['pattern'])
                ).all()

            # Search for property type
            elif args['type'] == 'property_type':
                result = query.filter(
                    SmaliProperty.property_type.contains(args['pattern'])
                ).all()

            # Search for property class
            elif args['type'] == 'property_class':
                result = query.filter(
                    SmaliProperty.property_class.contains(args['pattern'])
                ).all()

            else:
                log.error("Invalid search type: %s" % args['type'])
        else:
            result = query.all()

        return result

    def search_method(self, args={}):
        result = None
        query = self.db.query(SmaliMethod)

        # Search for method
        if ('type' in args) and ('pattern' in args):

            # Search for method id
            if args['type'] == 'id':
                result = query.filter(
                    SmaliMethod.id == int(args['pattern'])
                ).all()

            # Search for method name
            elif args['type'] == 'method_name':
                result = query.filter(
                    SmaliMethod.method_name.contains(args['pattern'])
                ).all()

            # Search for method type
            elif args['type'] == 'method_type':
                result = query.filter(
                    SmaliMethod.method_type.contains(args['pattern'])
                ).all()

            # Search for method class
            elif args['type'] == 'method_class':
                result = query.filter(
                    SmaliMethod.method_class.contains(args['pattern'])
                ).all()

            else:
                log.error("Invalid search type: %s" % args['type'])
        else:
            result = query.all()

        return result

    def search_call(self, args={}):
        result = None
        query = self.db.query(SmaliCall)

        # - Apply filters ----------------------------------------------------
        # from class
        if 'from_class' in args:
            if args['from_class']:
                log.debug("from_class = %s" % args['from_class'])
                query = query.filter(
                    SmaliCall.from_class.contains(args['from_class']))

        # from method
        if 'from_method' in args:
            if args['from_method']:
                log.debug("from_method = %s" % args['from_method'])
                query = query.filter(
                    SmaliCall.from_method.contains(args['from_method']))

        # to class
        if 'to_class' in args:
            if args['to_class']:
                log.debug("to_class = %s" % args['to_class'])
                query = query.filter(
                    SmaliCall.dst_class.contains(args['to_class']))

        # to method
        if 'to_method' in args:
            if args['to_method']:
                log.debug("to_method = %s" % args['to_method'])
                query = query.filter(
                    SmaliCall.dst_method.contains(args['to_method']))

        # local arguments
        if 'local_args' in args:
            if args['local_args']:
                log.debug("local_args = %s" % args['local_args'])
                query = query.filter(
                    SmaliCall.local_args.contains(args['local_args']))

        # destination arguments
        if 'dest_args' in args:
            if args['dest_args']:
                log.debug("dest_args = %s" % args['dest_args'])
                query = query.filter(
                    SmaliCall.dest_args.contains(args['dest_args']))

        # - Make query and return results ------------------------------------
        result = query.all()

        # Return results
        return result

    def xref_call(self, results, xref_type, max_depth=1):
        """ Get xref results """

        def to_xref(results):
            """ Get xrefs pointing _calling_ the results"""
            query = self.db.query(SmaliCall)

            # Unique class names
            class_names = list(set([r.from_class for r in results]))

            # Make query
            results = query.filter(SmaliCall.dst_class.in_(class_names)).all()

            return results

        def from_xref(results):
            """ Get xrefs which are __called__ by the results"""
            query = self.db.query(SmaliCall)

            # Unique class names
            class_names = list(set([r.dst_class for r in results]))

            # Make query
            results = query.filter(SmaliCall.from_class.in_(class_names)).all()

            return results

        # Avoid if blocks
        func_call = {'to': to_xref, 'from': from_xref}
        tmp_res = None

        # Get xrefs <max_depth> times
        for d in range(0, max_depth):
            if not tmp_res:
                tmp_res = func_call[xref_type](results)
            else:
                tmp_res = func_call[xref_type](tmp_res)

            log.info("Run:\t%d\tResults:\t%d" % (d, len(tmp_res)))

        # If no cross results, return old results
        return tmp_res if tmp_res else results
