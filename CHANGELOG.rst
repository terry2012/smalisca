**********
Changelog
**********


1.0-RC1 (2015-03-11)
====================

* Implemented basic project structure 
  
    * Basic CLI application
    * Use cement als stable CLI framework

* Add basic parsing functionalities 

    * Parse classes, methods, properties
    * JSONify results
    * No use of complex regexp (due to performance issues)

* Add filter functionalities

    * Search for classes, methods, properties
    * Create directed graphs (CFGs)

* Output results 

    * JSON
    * DOT (Graphviz)
