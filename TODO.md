# TODO

- [ ] Support for user-defined widget
- [ ] Default security (remove some \_\_builtins\_\_ from globals)
  * Limit default options for eval and exec (no IO nor import in builtins)
  * Prevent global code change from within the template?
    * see `safe_code` context manager (WIP)
    * Work with deep copy of object passed as parameters?
    * Limit them to mere data (dict, list, ... ?) 
  * We should never trust the template, neither expect the user to pass safe variables to template
- [ ] Clean up and simplify usage
- [ ] Automated unit tests (github workflow vs travis ?)
- [ ] Localy defined variables: current `<t-set>` defines global variables, we may want to defined variable for the current bloc only
- [ ] define `t-call` ? Strongly bind to the resolver