Tests
=====
This document aims to clarify what we are talking about when it comes to test the code.
Each time the topic is discussed between engineers or the rest of the team, it appears that there is no common understanding on what tests are, and thus, how, when and why we test.

This document expresses the ideas or views that should be understood and embraced by all, engineers or not.
 
Seriously
---------
Tests are the guarantee that the agreement between engineers, product people and customers is not broken.

The different techniques include:
 - __manual tests__: when someone checks the flow and business logic of the product
 - __functional tests__: when a script performs actions and validates the output
 - __unit tests__: when the behavior of each component is independently verified 

      _Other testing techniques are for example load testing, security testing..._

These techniques are like the *conditions*, the *loops* or the *assignments* of a programming language: no one prevails on the others, they have to be used together.

The __manual tests__ allow the product and engineering people to check and adjust their understanding on what the features and the underlying business logic are. Ideally they are designed by the product people and adjusted during the development cycle. They may be the reference for non-technical and technical people in order to understand what the system is supposed to do.

The __functional tests__ ensure that the flows and the results stay as they have been validated, over time and regardless of changes made anywhere in the product. The automation is essential, the repeatability is critical.

Finally the __unit tests__ help the reusability of the code, through valid and invalid inputs, and prevent unexpected minor changes that are difficult to proactively detect through high-level tests. Again, the automation is essential, the repeatability is critical.


Tasty tests
-----------
Though tests are costly, they are accepted as a huge part of the investment the company makes because tests provide more value than checking the stability of the product. 

Here is a list of some of the benefits that all stakeholders have to recognize, understanding that often the absence of tests causes the opposite of these benefits:
 - Force a coding style that detangles different purposes
 - Prevent to break untouched, but depending, parts
 - Allow (big) re-factors
 - Catch all programming errors
 - Avoid the ‘returning bug’ or the ‘that worked before’ feelings
 - Remove stress of all involved
 - Provide more accuracy to the team’s velocity
 - Define de facto always up-to-date documentation  

The common measure of tests are the number of assertions or the coverage percentage. If presented alone, they are misleading and should be ignored. Indeed, they may give a false sense of solid code. The discipline and the rigor of the engineers, as coders or reviewers, are fundamental.

Following a set of consistent approaches helps both coders and reviewers.
 
For example, for the __unit tests__:
 - Call `tested` what is tested - the method, the instance
 - Call `result` the result to check, call `expected` what is the expected result
 - Create at least one test method per method
 - For each assertion, add a comment describing it
 - Create the test methods in the order the methods appear in the code

There are also a few rules that help preventing fragile tests. 

For example, for the __unit tests__:
 - The test never computes the expected result the way the actual code does
 - The test may use constants as input, but never as the expected result
 - The test mocks all external components
 - The tests are independent of the order of execution

Tinker, hacker, coder, tester
-----------------------------
To keep this document short, here is a list of questions and answers.

Developers spend 50% or more of their time debugging released features.
>**False** - If this is the case, chances are that the time spent on tests is too short.

Developers spend 50% or more of their time writing tests.
>**True** - It is extremely rare that writing code takes more time than writing tests.

Tests should be written following all the good code practices (DRY, KISS..).
>**False** - Reusability, performance and all these code considerations are not the primary concern of good tests. The primary goals of tests are detecting incorrect functionalities and preventing regression. The mindsets of writing code and writing tests are different.

Only the important parts of the code need tests.
>**False** - Parts that don’t need tests should be removed. It is possible that a less important part of the code becomes important later. Odds are that no one will detect that and no one will diligently create the tests then.

Developers spend 80% or more of their time coding features.
>**False** - If this is the case, chances are that few tests would be written and that nobody would care about bugs.

End to end tests are enough since they cover more code surface and check the final output.
>**False** - The intermediary steps may be incorrect, e.g. the saved data. Additionally, bugs are more difficult to pinpoint and re-factors become enormous endeavours. 

Unit tests are enough since they check all code transformations.
>**False** - The coherence of the agglomerated functions is not guaranteed by the unit tests. Changing the flow will not be detected by the unit tests.

Any change of code should lead to test failures.
>**True** - If changing code does not fail the tests, then the tests were incomplete or incorrect. Reviewers should always see tests changes alongside code changes.

Tests should be written before any code.
>**False** - The order, code or tests, depends totally on the context. Tests are not after thoughts, but may be written at the end.

Flaky tests are acceptable because they eventually succeed.
>**False** - When successful, a flaky test just proves that the code works as wanted, sometimes.   

Testing the third-party code - packages, frameworks - is adding confidence.
>**False** - There are boundaries to tests, external code is one of them. Of course, it is important to ensure that the third-parts have their own tests.   

Code should never be released without tests.
>**False** - Code fix may be applied without tests to prevent further breaks. But, the immediate following task should be to write the tests to validate the code fix.
