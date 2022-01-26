# XMLego

* inspired by [Odoo templating](https://www.odoo.com/documentation/15.0/developer/reference/frontend/qweb.html)
* Name: XML + Lego; Extend you template without limit



## Why another template engine?

There are plenty of very good template engine such as [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) or [Mako](https://www.makotemplates.org/), but I needed something that would allow a template to choose where it would hook on its parent. All the templating I've tried only allowed me to define slots on a template.

That is absolutely all there is to say. 

The module is inspired by [Odoo QWeb Templates](https://www.odoo.com/documentation/15.0/developer/reference/frontend/qweb.html) which I have been working with for +3years. The QWeb templating is deeply bound to the ERP and is not made available for itself. IMO, it suffers from its legacy code, that is way only the behaviour is reproduced, but not the code.



## Fonctionnalities: 2 separated parts



### Inheritance handling

Takes multiple templates, resolve order and dependency, prevent cyclic dependency and merge them together **without any other processing**.
The dependency order resolution is done using a reversed topological sort. I plan to add other resolution based on dfs and bfs iterations and maybe other solutions.

This requires xml format, this won't be by **itself** (see below the templating part) of any use if you need another kind of format.
But then, you can use any templating engine you want on the merged result



### Templating

What if you want to merge files with a final format different than xml?
Response:

1. Put some transient tags `<t id="myid"></t>` to provide many hooks for you children
2. Handle inheritence
3. Post-process by removing the transient tags with `remove_transient_tags` methode
4. Extract the content

#### Is that all? No!

I was already to deep into it and couldn't stop myself from implementing the following features (see the exemple below)

* Foreach-loop: Impoved from Odoo, you can assign multiple variable per loop
* Global variable declaration/asssignation
* Conditional if, elif and else
* Render text
* Attribute evaluation (any attribute starting with `t-att-`)



## Performance

No current benchmark, certainly not as good as other template engines



## Current State

Even if this is a fully working: This is still a 3h project with no real big thinking about implemention.
My next priorities are:

1. Check security issues from `exec` and `eval` to add a safe default
2. Clean it up
3. Make it easier to use (wrap utilities, handler/context manager, etc)
4. Improve performance



## Exemple

The following xml (without additionnal variables)...

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xmlego>
    <template id="mytemplate1">
        <div id="mydiv1">
            test
        </div>
    </template>
    <template id="mytemplate2" inherits="mytemplate1">
        <xpath expr="div[@id='mydiv1']" position="after">
            <div id="mydiv2">
                test2
            </div>
        </xpath>
    </template>
    <template id="mytemplate3" inherits="mytemplate2">
        <xpath expr="div[@id='mydiv2']" position="after">
            <div id="mydiv3">
                test3
            </div>
        </xpath>
    </template>
    <template id="mytemplate4" inherits="mytemplate2">
        <xpath expr="div[@id='mydiv2']" position="after">
            <div id="mydiv4">
                <t-set value="0" as="mysum"/>
                <div t-foreach="(i, i + 5) for i in range(7)" t-as="i, j">
                    <div t-text="i" t-att-class="'class' + str(i)">test loop </div>
                    <t-set value="mysum + j" as="mysum"/>
                    <div t-text="mysum" >current sum: </div>
                    <br/>
                    <br/>
                    <div t-text="i" >current index: </div>
                    <div t-if="not i % 2"> MOD 2!</div>
                    <div t-elif="not i % 3"> MOD 3!</div>
                    <div t-else=""> Not Mod 2 nor Mod 3</div>
                </div>
            </div>
            <div t-text="mysum" >final sum: </div>
        </xpath>
    </template>
</xmlego>
```



Will produce the following output:

```xml
<template id="mytemplate1">
        <div id="mydiv1">
            test
        </div><div id="mydiv2">
                test2
            </div><div id="mydiv3">
                test3
            </div>
        <div id="mydiv4">
                <div><div class="class0">test loop 0</div>
                    <div>current sum: 5</div>
                    <br/>
                    <br/>
                    <div>current index: 0</div>
                    <div> MOD 2!</div>
                    <div class="class1">test loop 1</div>
                    <div>current sum: 11</div>
                    <br/>
                    <br/>
                    <div>current index: 1</div>
                    <div> Not Mod 2 nor Mod 3</div>
                <div class="class2">test loop 2</div>
                    <div>current sum: 18</div>
                    <br/>
                    <br/>
                    <div>current index: 2</div>
                    <div> MOD 2!</div>
                    <div class="class3">test loop 3</div>
                    <div>current sum: 26</div>
                    <br/>
                    <br/>
                    <div>current index: 3</div>
                    <div> MOD 3!</div>
                    <div class="class4">test loop 4</div>
                    <div>current sum: 35</div>
                    <br/>
                    <br/>
                    <div>current index: 4</div>
                    <div> MOD 2!</div>
                    <div class="class5">test loop 5</div>
                    <div>current sum: 45</div>
                    <br/>
                    <br/>
                    <div>current index: 5</div>
                    <div> Not Mod 2 nor Mod 3</div>
                <div class="class6">test loop 6</div>
                    <div>current sum: 56</div>
                    <br/>
                    <br/>
                    <div>current index: 6</div>
                    <div> MOD 2!</div>
                    </div></div>
            <div>final sum: 56</div>
        
        
    </template>

```

