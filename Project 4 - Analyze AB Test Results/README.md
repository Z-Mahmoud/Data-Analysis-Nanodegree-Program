## Introduction

A/B tests are very commonly performed by data analysts and data scientists. 
We will be working to understand the results of an A/B test run by an e-commerce website.  
Our goal is to work through this notebook to help the company understand if they should:
- Implement the new webpage, 
- Keep the old webpage, or 
- Perhaps run the experiment longer to make their decision.

### I- Using Probability
**We don't have statistical evidence that the new `treatment` group users lead to more conversions, but we suggest to run the test for longer period**
- This test split all users into two almost equal sized groups (control 49.994%, treatment 50,006%).
- The conversion rates for the two groups are very close (control 12.04%, treatment 11.88%).
- The actual difference between the conversion rates for the two groups is around 0.16% in favor of the control group.
- The duration of the test was 22 days.
- We need to consider the novelty effect and change aversion.

### II- Using A/B Test
 - The hypotheses
    - `$H_0: p_{new} - p_{old} \leq 0$`
    - `$H_1: p_{new} - p_{old} > 0$`

We computed the P-value, it defined as the probability of getting our statistic or a more extreme value if the Null Hypothesis is true

With large P-value (like in our case 90.38%) we do not have evidence to reject the null Hypothesis, in other terms we can't say that the new page lead to more conversion rate, especially after comparing the computed P-value to the Type I error rate α (5%), as we can reject the null only if `pval ≤ α`

**using statsmodels ztest**
From the z-score and p-value that we computed, we still do not have evidence to reject the null Hypothesis
- Our hypothesis is right-tailed test so `𝑍𝛼 = 1.645`
- For a right-tailed test, reject null if  `𝑍𝑠𝑐𝑜𝑟𝑒  >  𝑍𝛼`.
- 𝑍𝑠𝑐𝑜𝑟𝑒 is less than 𝑍𝛼
- We have large P-value


### III- Using A regression approach
- The p-value associated with ab_page = 0.1899, and it differ from the value we found in A/B Test as it's for diffrent hypotheses
- The hypothesis test for our regression model is a test of if the Correlation Coefficient between the `landing_page` and `converted` columns equal to zero or differs from zero
    - If p-value < Type I error rate (0.05) then we can reject the null hypothesis, in other terms "this variable has a statistically significant relationship with the response"
- the hypothesis in Part II are one-sided and the hypothesis in Part III are two-sided
- In our regression model, the computed p-value associated with ab_page (0.1899) is greater than Type I error rate (0.05), we do not have evidence to reject the null Hypothesis, in other terms we can't say that the new page lead to more conversion rate

#### Consider other factors to add into the regression model
- Choosing the correct factors prevent us from taking misguided decisions that will harm the company's in the long run.
    - We should also take in consideration the practical significance not only the statistical.
    - We need to consider the novelty effect and change aversion.
    - We need to consider the duration of our test.
    <br><br>
- When adding additional terms into our regression model, we should be aware of some of the problems that we might face like
    - The relationship may not exist.
    - Outliers.
    - Multicollinearity (predictor variables should be correlated with the response, but not with one another).

#### Adding an effect based on which country a user lives in
- All p-values in the summary is greater than Type I error rate (0.05), we do not have evidence to reject the null Hypothesis, in other terms we can't say that changing the page or the country effects the conversion rate
- We predict that if a user visit the old page, they are 1.015 more likely to convert than if they visit the new page, holding all other variables constant (same country).
- We predict that users from US are 1.042 more likely to convert than users from CA, holding all other variables constant (same group/landing_page).
- We predict that users from UK are 1.010 more likely to convert than users from US, holding all other variables constant (same group/landing_page).

#### Looking at an interaction between page and country to see if are there significant effects on conversion
- All p-values in the summary is greater than Type I error rate (0.05), we do not have evidence to reject the null Hypothesis
- In other terms we can't say that there's interaction between `country` and `landing_page` that will help predict user conversion
<br><br>

## Conclusion

- **After analysing the results of this A/B test using diffrent methods:**
    - There's no sufficient evidence to reject the null Hypothesis.
        - We can't say that the new page lead to more conversion rate.
    - UK has small statistical increase in conversion rate with the new page, however it's not enough to consider it practically useful.
    - We recommend the company to run the experiment longer to make their decision, further analysis also should include the influences associated with time on conversion.
