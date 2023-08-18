
what is prior predictive distribution?
- Prior predictive checks generate data according to the prior in order to asses whether a prior is appropriate
- it is the distribution of the data that we would expect to see if we were to sample from the prior distribution
- https://mc-stan.org/docs/2_26/stan-users-guide/prior-predictive-checks.html


what is posterior predictive distribution?
- it is the distribution of the data that we would expect to see if we were to sample from the posterior distribution

what is NUTS sampler?
- it is a sampler that is used to sample from the posterior distribution

what is HDI in bayesian?
- it is the highest density interval, which is the interval that contains the 95% of the posterior distribution

what is the difference between bayesian and frequentist?
- bayesian: we have a prior belief about the parameter, we update our belief based on the data, we have a posterior belief about the parameter
- frequentist: we don't have a prior belief about the parameter, we estimate the parameter based on the data

what is the difference between bayesian and frequentist in terms of hypothesis testing?
- bayesian: we have a prior belief about the parameter, we update our belief based on the data, we have a posterior belief about the parameter, we can test the hypothesis by comparing the posterior distribution of the parameter with the null hypothesis
- frequentist: we don't have a prior belief about the parameter, we estimate the parameter based on the data, we can test the hypothesis by comparing the estimate of the parameter with the null hypothesis

what is the difference between bayesian and frequentist in terms of confidence interval?
- bayesian: we have a prior belief about the parameter, we update our belief based on the data, we have a posterior belief about the parameter, we can calculate the HDI of the posterior distribution of the parameter
- frequentist: we don't have a prior belief about the parameter, we estimate the parameter based on the data, we can calculate the confidence interval of the estimate of the parameter

what is the difference between bayesian and frequentist in terms of prediction?
- bayesian: we have a prior belief about the parameter, we update our belief based on the data, we have a posterior belief about the parameter, we can calculate the posterior predictive distribution
- frequentist: we don't have a prior belief about the parameter, we estimate the parameter based on the data, we can calculate the prediction interval of the estimate of the parameter

what is MCMC method?
- it is a method that is used to sample from the posterior distribution
 
how does it work?
- it starts from a random point in the parameter space, it proposes a new point in the parameter space, it accepts the new point if it is more likely than the previous point, it accepts the new point with a probability if it is less likely than the previous point, it repeats this process until it converges to the posterior distribution

what is the difference between MCMC and NUTS?
- MCMC is a method that is used to sample from the posterior distribution, NUTS is a sampler that is used to sample from the posterior distribution





To change my shell from zsh to bash, I did the following:
  - open terminal
  - type: chsh -s /bin/bash
  - close terminal and open it again
To change my shell from bash to zsh, I did the following:
  - open terminal
  - type: chsh -s /bin/zsh
  - close terminal and open it again and you should see 
  (base) SCXMACKHALILZADEHA:~ khalilza$ instead of 
  (base) khalilza@SCXMACKHALILZADEHA ~ % 

to create a new conda env:
  - conda env create -f workshop.yml
  - conda activate adsml
  - it took 15 minutes in my mac to create the env

to remove a conda env:
  - conda remove -name workshop --all




env:
 to make sure I run the qmd file within the workshop env, I did the following:
 - in vs code, open Setting
 - in search bar, search for python extension
 - under the Default Interpreter Path enter
 /Users/khalilza/miniconda3/envs/workshop/bin/python
 I installed the jupyter-cache in the workshop env, so even if my qmd doesn't contain any python code, but for caching to work, the cache extension is needed. Hence, the render should be done once I am in the workshop env. Setting the path as described above will ensure that. Nevertheless, the jupyter-cache can be also installed in the base.

things installed:
# to use the cache feature of quarto
https://pypi.org/project/jupyter-cache/
- pip install jupyter-cache 

# to be able to use shiny in a server
https://docs.posit.co/shinyapps.io/getting-started.html#working-with-shiny-for-python
- pip install rsconnect-python 

# to use shiny in python
- in workshop env: pip install shinylive --upgrade 
- in workshop follder: quarto install extension quarto-ext/shinylive
- in workshop folder create _quarto.yml and write 
filters:
  - shinylive

to use shiny in slides:
sharing: https://shiny.posit.co/py/docs/shinylive.html
examples: https://shiny.rstudio.com/py/


refs:
- https://www.youtube.com/watch?v=HZGCoVF3YvM
- https://www.youtube.com/watch?v=0F0QoMCSKJ4&list=PLN5IskQdgXWktwVOxs3vAVkI4jpMX3pIv&index=2
- quarto blog: https://meghan.rbind.io/blog/quarto-slides/
- quarto blog: https://www.apreshill.com/blog/2022-04-we-dont-talk-about-quarto/
- quarto blog: https://mine-cetinkaya-rundel.github.io/quarto-tip-a-day/
- quarto blog https://apps.machlis.com/shiny/quartotips/
- quarto blog https://www.emilhvitfeldt.com/post/slidecraft-code-output/
- quarto blog https://www.emilhvitfeldt.com/post/slidecraft-colors-fonts/#finding-fonts
- CAPE https://drive.google.com/drive/u/0/folders/11FSi-4A0EXdM6_WshwGNud9q34UPzG3Q


helpers
- to add background image: {background-image="img/handson.png" background-size="cover"}
- frequentism: Ronald Fisher (1890-1962), bayesianism: Thomas Bayes (1702-1761), Pierre-Simon Laplace (1749-1827)
- to change font color [QA]{style="color:white;"}
- new line
- create QA and hands-on time as an repeated slide https://mine-cetinkaya-rundel.github.io/quarto-tip-a-day/posts/04-include/
- ## Fragments

::: columns
::: {.column width="50%"}
[This shows up first,]{.fragment fragment-index="1" style="color:orange;"}
:::

::: {.column width="50%"}
[then this,]{.fragment fragment-index="2" style="color: blue;"}
:::
:::

[then this.]{.fragment fragment-index="3" style="color: pink;"}

##  {#slide1-id data-menu-title="coffee break"}

::: {style="font-size: 5em; font-color: #32a6a8 ;text-align: center"}
Coffee Break <br> :coffee:
:::



how to explain the with statement in pymc?

the pymc code looks like this: it hijacks the context manager which one usually uses for 
opening/closing files and instead uses it to create a context for the model and define its variables. Here it opens a model (WITH pm.Model() AS model)
and populate it with the priors and variables. Then it runs the model and samples from the posterior. 
Model is an object which is a container  for the model random variables. It is the top level container for all probability models. 

Finally it returns the posterior samples. The context manager is a python construct that
allows you to do something before and after a block of code. In this case it opens the model
and closes it after the sampling is done.
Any time you declare a pymc mvariable inside a with statement (or context manager), it gets added to the model. Pymc is a high level language.

how to explain the MCMC method? 
- But what if our prior and likelihood distributions weren’t so well-behaved?
- it is a class of algos that are used to sample from the posterior distribution. 
- It approximates the posterior distribution.
- It samples from markov chain. 
- it does random sampling in a probabilistic space.
- Most famous algo is metrapolis sampling. 
- There is also gibs.
- It randomly select values (random walk), and evaluates them.
- If the new value is more likely than the previous value, it accepts the new value.
- The trick is that, for a pair of parameter values, it is possible to compute which is a better parameter value, by computing how likely each value is to explain the data, given our prior beliefs. If a randomly generated parameter value is better than the last one, it is added to the chain of parameter values with a certain probability determined by how much better it is (this is the Markov chain part).

https://www.youtube.com/watch?v=911d4A1U0BE&t=1155s


to check what makes code slow, I uninstalled the following extensions:
- jupyter slide show
- Jupyter Notebook Renderers
- Jupyter Keymap
- Jupyter Cell Tags

- Material Icon Theme


quarto questions:
- how to change text-selection color?
- how to fit the backgrund image to the slide? the cover and contain doesn't work


how to design hands on sessions:
- start with simple things which can be done individually (in DAY1) and then move to more complex things which can be done in groups (in DAY2)
- there should be a clear goal for each hands on session
- there should be a clear time limit for each hands on session
- there should be atleast a session where they do things on their own, and I will be there to help them only




