## P01: ArRESTed Development
### Due: TBD

_Imagine:_

_Your team has been contracted to showcase your company's proficiency with frontend frameworks and RESTful APIs. You have secured creative freedom of expression, constrained only by the bounds of scholarly discourse and these terms, upon which you have agreed:_
* Flask will serve as your web microframework.
* Multiple supporting Python3 files will be used as necessary.
* Bootstrap|Foundation|Tailwind will serve as your front-end framework.
* You will provide your own customized CSS where appropriate/necessary.
* You will make _meaningful_ use (sum > parts) of at least three (3) REST APIs, chosen from Ye Olde SoftDev API KB.

----- 

Your "software solution," to use the parlance of our times, will incorporate a few distinct components, so it is imperative that your team develop a design and agree upon roles ___before___ you move to implementation. Your team's first order of business is reaching agreement as to how your project will be organized and how you will divide work. It will be imperative you have a shared organizational model of your target, so that each teammate shares the same organizational model of your target and understand how they and their work will fit into it. Express your plan in a _design document_.

(___Nota bene:___ _This is your first non-housekeeping deliverable. All your efforts should be directed to doing this job well; do not spend time working on other aspects of the project until design docs have been developed, reviewed, revised._)
<br>

### Design Document Specifications:
- A *list* of program components with role of each specified. (e.g., a car engine is comprised of various components: carburetor, alternator, radiator, spark plugs, etc. Each must perform its role for the engine to do its overall job.)
- Explanation of how each component relates to the others.
  - Component map visualizing relationships between components.
- Database Organization (tables? Relationships b/t tables? etc.)
- Site map for front end
  - Represent each page you envision for your site.
  - Show linkages conveying all possilbe pathways for a user traversing site.
- A breakdown of the different tasks required to complete this project
  - Include assignments of each task to each group member
- Clearly labeled section delineating APIs you will use.
- Clearly labeled section noting which front-end framework you will use and why/how. (_E.g._, Which of its features do you plan to make integral use of? Which might you use, if appropriate or time-permitting?)
- Append this line to your heading: **`TARGET SHIP DATE: {yyyy-mm-dd}`**
- Amalgamate these components into a single PDF, store in designated location.

### Project Guidelines:
* Flask will serve as your web server/delivery framework.
* SQLite3 will serve as your backend data storage system.
* At minimum, your database component will facilitate user accounts.
* Multiple Python files should be used, as necessary, for application layer. (_a.k.a._ "middleware" modules, etc.)
* FEF: Bootstrap|Foundation|Tailwind
* RESTful APIs:
  - At least 3.
  - Get creative, think boldly: 1+1+1+1 -> 7!
  - Pre-requisite reminder: Any APIs used must have a card in Devo Nation local KB.
* CSS: Write as much as you like.
  - If you must copy existing CSS, cite your source
  - your site must function with CSS stripped away.
* Use Q&A forum liberally. *"A rising tide lifts all boats."*
* _Reminder:_ include heading as comment in all source files.
* Platinum Rule: __THOUST APP SHALT NOT FAIL.__

Your website will incorporate a few distinct components, so it is imperative that your team develop a design and agree upon roles ___before___ you move to implementation.

----- 

You will need a DEVLOG for this project.
* Devlog allows any group member at any time to see the current state of the project.
* PM will make sure devlog is being maintained, but will not make all entries.
* The devlog should be a plain text file, stored in the specified location.
* When any team member stops working and pushes changes to github, they should update the devlog explaining what changes have been made. Include errors/bugs discovered (or created).
* Separate devlog entries with a newline.
* Most recent entry at the bottom.
* Each entry should begin with the following format: `firstL -- TIMESTAMP\n` ( _e.g._: `topherM -- 1999-12-31 23:59` )

----- 

### FINAL DELIVERABLES (watch this section for updates):

* hardcopy:
  * final version of design doc (x1)
  * staple because it indicates "you have it together"
* repo structure:
```
app/
    __init__.py
    static/
        css/
        js/       (SITUATION-DEPENDENT: IF YOU REALLY NEED MINIMAL JS, IT WILL GO HERE)
    templates/
    keys/
        readme
        key_<api-name>.txt
        key_<api-name>.txt
        key_<api-name>.txt
design.pdf
devlog.txt
flag.jpg
README.md
requirements.txt
```
* `README.md`
  * Clearly visible at top: __\<Project Name\> by \<Team Name\>__
  * Roster with roles
  * Description of website/app (a la abstract of a scientific paper... NOT your entire design doc!)
  * Install guide:
    * How to clone/install.
  * Launch codes:
    * How to run.
* `design.pdf`
  * Latest/current version of your design document.
  * Revisions since v0 noted/explained in devlog.
* `requirements.txt`
  * It will list flask as well as any other pip installs your app requires.
  * Latest version of all packages.
  * Clearance must be sought and granted for any modules/libraries not explicitly covered in class.

----- 

### Subgoals / Checkpoint Deliverables:

1. `T 2024-11-26t 08:00`
   - submodule linked
   - team registered
   - team flag in place
1. `W 2024-11-27w start of class`
   - deposit hardcopy of design doc (3x) on lisadesk by start of class period
   - writing utensils of multiple non-blue/black hues
1. `T 2024-12-03t 08:00`
   - revised design document
   - summary of design doc changes in devlog
   - deposit hardcopy of design doc (1x) on lisadesk at beginning of pd
   - readme heading

----- 

related:
<br>
[tk](https://)
