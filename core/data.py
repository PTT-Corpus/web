"""Data for `boards` autocomplete."""
import json
from pathlib import Path
# boards = ['joke', 'movie', 'marvel', 'Tech_Job', 'japanavgirls', 'Hearthstone', 'KR_Entertain', 'Beauty', 'Hip-Hop', 'Steam', 'HardwareSale', 'Japan_Travel', 'MakeUp', 'Japandrama', 'Salary', 'marriage', 'NSwitch', 'Tennis', 'Kaohsiung', 'e-shopping', 'Monkeys', 'MuscleBeach', 'BabyMother', 'BTS', 'Boy-Girl', 'TaichungBun', 'MLB', 'home-sale', 'China-Drama', 'PC_Shopping', 'YuanChuang', 'ToS', 'Tainan', 'iOS', 'PokemonGO', 'Gossiping', 'HatePolitics', 'WomenTalk', 'SportLottery', 'TY_Research', 'creditcard', 'FATE_GO', 'MobileComm', 'Baseball', 'KoreaDrama', 'WOW', 'Guardians', 'BeautySalon', 'CFantasy', 'KoreaStar', 'StupidClown', 'PlayStation', 'AllTogether', 'BuyTogether', 'sex', 'C_Chat', 'car', 'Stock', 'Wanted', 'AKB48', 'KanColle', 'ChungLi', 'BabyProducts', 'GetMarry', 'Lifeismoney', 'give', 'Zastrology', 'Gamesale', 'LoL', 'Hsinchu', 'AC_In', 'MacShop', 'basketballTW', 'CVS', 'HelpBuy', 'CarShop', 'part-time', 'cat', 'nb-shopping', 'Elephants', 'mobilesales', 'TaiwanDrama', 'DC_SALE', 'lesbian', 'IdolMaster', 'MobilePay', 'Headphone', 'DMM_GAMES', 'Palmar_Drama', 'Teacher', 'Food', 'cookclub', 'gay', 'shoes', 'NBA', 'PublicServan', 'DSLR', 'Aviation', 'MH', 'EAseries', 'Storage_Zone', 'Isayama', 'Finance', 'PRODUCE48', 'GirlsFront', 'StarCraft', 'ONE_PIECE', 'biker', 'MayDay', 'NBA_Film', 'Examination', 'PCReDive', 'BigBanciao', 'watch', 'fastfood', 'LGBT_SEX', 'PathofExile', 'Soft_Job', 'RealmOfValor', 'CN_Entertain', 'Gov_owned', 'PuzzleDragon', 'TypeMoon', 'TW_Entertain']  # noqa: E501
boards = []
for board in Path("/app/cwb/registry").iterdir():
    boards.append(board.name)

#boards = ['BabyMother', 'LGBT_SEX']
#boards = {k: None for k in boards}
#boards = json.dumps(boards)
boards = [(board, board) for board in boards]
