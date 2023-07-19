# Capture The Flag!

**Solve challenges to get flags for a scorebot**

**Assignment 2** for **[Computer Networking](https://search.usi.ch/en/courses/35263648/computer-networking)**
course during the Spring Semester 2022 @ [USI Università della Svizzera italiana](https://www.usi.ch).

* Aristeidis Vrazitoulis: [vrazia@usi.ch](mailto:vrazia@usi.ch)
* Marina Papageorgiou: [papagm@usi.ch](mailto:papagm@usi.ch)
* Diego Barreiro Perez: [barred@usi.ch](mailto:barred@usi.ch)

_All code is properly documented with extensive inline and definition comments._


### Installation

No specific installation instructions are required. Just install a **`Python 3`** version.

### Running

To run a specific challenge, you may type the following command (where `N` is a number between _1_ and _10_, specifying
the challenge number):

```bash
python client_N.py
```

To run and automatically submit a challenge's flag (**bonus task**),you may run the following command (replacing
`incognito.guy` with the desired username, and `N` with the challenge number):

```bash
python submit.py -u incognito.guy -c N
```

Alternatively, to run and submit all challenges, you may omit the `-c` flag (it will execute challenges _1_ to _10_):

```bash
python submit.py -u incognito.guy
```

These are all the available options for the scorebot submitter:

```bash
PS C:\Github\NTW22-2> python submit.py -h
usage: submit.py [-h] -u USERNAME [-c [1-10]]                                                              
                                                                                                           
Scorebot Submitter                                                                                         
                                                                                                           
optional arguments:                                                                                        
  -h, --help            show this help message and exit                                                    
  -u USERNAME, -U USERNAME, --username USERNAME                                                            
                        username of the user to which the flag(s) will be registered                       
  -c [1-10], --challenge [1-10]                                                                            
                        challenge of which the flag will be submitted (if none, it will submit all of them)
PS C:\Github\NTW22-2>
```
