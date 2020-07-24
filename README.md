# Mutual-Funds-Moving-Average-Webapp 💹
## Table of Contents
  * [Disclaimer](#disclaimer)
  * [Demo](#demo)
  * [Overview](#overview)
  * [Motivation](#motivation)
  * [Technical Aspect](#technical-aspect)
  * [Installation](#installation)
  * [Run](#run)
  * [To Do](#to-do)
  * [Bug / Feature Request](#bug--feature-request)
  * [Technologies Used](#technologies-used)
  * [Team](#team)
  * [Credits](#credits)


## Disclaimer
⚠️
**This webapp is made for knowledge purposes only and should not be considered as investment advice.**

**Please perform your own research before making any decisions.**

## Demo
Link: [https://mutual-funds-moving-avg-webapp.herokuapp.com/](https://mutual-funds-moving-avg-webapp.herokuapp.com/)

[![](https://i.imgur.com/lCzMe80.png)](https://mutual-funds-moving-avg-webapp.herokuapp.com/)

## Overview
In financial applications a [simple moving average (SMA)](https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average) is the unweighted mean of the previous n data. An example of a simple equally weighted running mean for a n-day sample of closing price is the mean of the previous n days' closing prices.

It is a simple technical analysis tool that smooths out NAV by creating a constantly updated average NAV. The average is taken over a specific period of time, like 10 days, 20 minutes, 30 weeks or any time period the investor chooses. Here, we choose the short term indicator as 6 month moving average(6MMA) and long term indicator as 12 month moving average (12MMA).

The basic idea is: **If the current value of 6MMA of a fund is greater than or equal to it's 12MMA, we buy for that particular month. Otherwise if current value of 6MMA is less than it's 6MMA, we sell redeem completely from the fund and move to fixed income.** This principle is known as **Momentum Investing**. This approach is only useful for equity oriented funds for reducing risk (standard deviation).


## Motivation
TODO

## Technical Aspect
TODO

## Installation
TODO

## Run
TODO

## To Do
1. Update the readme with better documentation.
2. Update the NAV value everyday (currently NAV value is static).

## Bug / Feature Request
If you find a bug (the website couldn't handle the query and / or gave undesired results), kindly open an issue [here](https://github.com/vneogi199/Mutual-Funds-Moving-Average-Webapp/issues/new) by giving as much detail as possible regarding the issue.

If you'd like to request a new function, feel free to do so by opening an issue [here](https://github.com/vneogi199/Mutual-Funds-Moving-Average-Webapp/issues/new). 

## Technologies Used

![](https://forthebadge.com/images/badges/made-with-python.svg)

TODO

## Team
TODO


## Credits
TODO



