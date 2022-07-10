Recycle Incentive Telegram Bot
=====================
By Ivan Koh, Valentin Khoo, Chong Kaiyu, Bandy Tan
Life Hack 2022

* **[Devpost Link](https://devpost.com/software/r-easy-cle)**

## Inspiration
Many Singaporeans are unaware of the main 2 initiatives put in place to incentivise Singaporeans to recycle more: [The E-waste National Recycling Program](https://www.nea.gov.sg/our-services/waste-management/3r-programmes-and-resources/e-waste-management/where-to-recycle-e-waste) and the [Cash-for-Trash Program](https://www.nea.gov.sg/our-services/waste-management/3r-programmes-and-resources/recycling-collection-points). 

**We believe that greater awareness and accessibility of these initiatives will encourage Singaporeans to be involved in recycling efforts.**

### We have identified the following issues:
- Recycling E-waste can be quite cumbersome as there are many different categories of e-waste, and not all can be processed together. 
- Furthermore, not all E-waste recycling points accept all categories of e-wastes, so one would have to take additional effort to search for a suitable recycling point. 

*What if there was an application that can provide directions to the nearest collection point with a touch of a button?*.

- Additionally, Cash-for-Trash stations can be a hassle as they are not easy to locate 
- Obtaining information can be difficult due to the Cash-for-Trash program being run by 3 separate companies. 

*What if there as an application that can reduce this hassle by providing detailed information on Cash-for-Trash with a touch of a button?*

## What it does
Have a bunch of e-wastes to recycle but need help with directions? Want to redeem cash for recylable materials but not sure where to go? Simply share your location with our Telegram bot and let it settle everything else for you. Quickly find recycling spots near you with our Telegram bot, R(easy)cle! 

R(easy)cle is a user-friendly Telegram bot that helps you find recycling spots near you. All that is required is to select the type of recycling spot of your choice, and with a tap of your screen R(easy)cle will show you the way!

## How we built it
- The R(easy)cle telegram bot was built using the '''python-telegram-bot''' API on '''Python'''
- Python Pandas was largely used to perform data retrieval and manipulation.
- Data Sources: [OneMap](https://www.onemap.gov.sg/docs/) and [NEA](https://www.nea.gov.sg/our-services/waste-management/3r-programmes-and-resources/recycling-collection-points)
