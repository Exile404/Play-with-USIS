from Backend.backend import Usis


with Usis() as bot:
    bot.land_first_page()
    bot.login('nfsdhrubo@gmail.com','^^^')
    bot.seat_status_option()
    bot.seat_stattus_selection('2022','Fall 2022','CSE220')

    bot.courses_list()































