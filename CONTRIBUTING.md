# Contributing
You are more than welcome to contribute this project! Please use the issue tracker, or email to reach out and discuss
your ideas. 

If you are contributing new code, then 
1. First, fork the repository and create your own branch. Commit your changes to
   this branch. 
2. In your commit, please include a test case that demonstrates that your
   contribution works as expected using `pytest`.
   Having a test case will make it easier to review your code and therefore lead
   to your pull request being approved faster.  Please also use `pylint` to check
   for issues. During development it is usually simplest to disable
   reports via `pylint my_feature.py --reports=n` and then enable again once all
   issues have been corrected. Make sure that you test all parts of your code
   using a coverage tool such as `py-cov`.
3. Update [ACKNOWLEDGMENTS](ACKNOWLEDGMENTS.md) to make sure you get credit for
   your contribution. 
4. Update [README](README.md) to explain how to use your feature.
5. Make all your commits to your feature branch and check that all tests pass.
   Then go ahead and submit a pull request! 
