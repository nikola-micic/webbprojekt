from django.core.management.base import BaseCommand, CommandError
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from core.models import Game, Team, Pick, CustomUser
nba_teams = {'Hawks': 'Atlanta', 'Celtics': 'Boston', 'Nets': 'Brooklyn', 'Hornets': 'Charlotte', 'Bulls': 'Chicago', 'Cavaliers': 'Cleveland', 'Mavericks': 'Dallas', 'Nuggets': 'Denver', 'Pistons': 'Detroit', 'Warriors': 'Golden State', 'Rockets': 'Houston', 'Pacers': 'Indiana', 'Clippers': 'Los Angeles', 'Lakers': 'Los Angeles', 'Grizzlies': 'Memphis', 'Heat': 'Miami', 'Bucks': 'Milwaukee', 'Timberwolves': 'Minnesota', 'Pelicans': 'New Orleans', 'Knicks': 'New York', 'Thunder': 'Oklahoma City', 'Magic': 'Orlando', '76ers': 'Philadelphia', 'Suns': 'Phoenix', 'Trail Blazers': 'Portland', 'Kings': 'Sacramento', 'Spurs': 'San Antonio', 'Raptors': 'Toronto', 'Jazz': 'Utah', 'Wizards': 'Washington'
}

class Command(BaseCommand):
    help = "Scrapes past and upcoming NBA games"
    
    def handle(self, *args, **options):
        def scrape_past_games():
            base_url = "https://www.nba.com/games?date="
            date_yesterday = datetime.date.today() - datetime.timedelta(days=1)
            date_today = datetime.date.today()
            dates = [date_yesterday, date_today]
            for date in dates:
                url = base_url + str(date)
                driver = webdriver.Firefox()
                driver.get(url)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                games = soup.find_all("div", class_="GameCard_gc__UCI46 GameCardsMapper_gamecard__pz1rg")
                driver.close()
                for game in games:
                    game_object = Game()
                    team_names = game.find_all("span", class_="MatchupCardTeamName_teamName__9YaBA")
                    team_names_clean = [tag.get_text() for tag in team_names]
                    team_scores = game.find_all("p", class_="MatchupCardScore_p__dfNvc GameCardMatchup_matchupScoreCard__owb6w")
                    team_scores_clean = [tag.get_text() for tag in team_scores]
                    if len(team_scores_clean) < 2:
                        break

                    home_team_name = nba_teams.get(team_names_clean[1]) + " " + team_names_clean[1]
                    home_team = Team.objects.get(name=home_team_name)
                    home_team_score = int(team_scores_clean[1])
                    away_team_name = nba_teams.get(team_names_clean[0]) + " " + team_names_clean[0]
                    away_team = Team.objects.get(name=away_team_name)
                    away_team_score = int(team_scores_clean[0])
                    if home_team_score > away_team_score:
                        winner = home_team
                        loser = away_team
                    elif away_team_score > home_team_score:
                        winner = away_team
                        loser = home_team

                    try:
                        game_check = Game.objects.get(home_team=home_team, away_team=away_team, date=date)
                        Game.objects.filter(home_team=home_team, away_team=away_team, date=date).update(winner=winner, home_team_score=home_team_score, away_team_score=away_team_score)
                        Pick.objects.filter(game=game_check, team_picked=winner).update(successful_pick=True)
                        Pick.objects.filter(game=game_check, team_picked=loser).update(successful_pick=False)
                        correct_picks = Pick.objects.filter(game=game_check, successful_pick=True)
                        false_picks = Pick.objects.filter(game=game_check, successful_pick=False)
                        for pick in correct_picks:
                            user = CustomUser.objects.get(id=pick.user_id)
                            CustomUser.objects.filter(id=user.id).update(successful_picks= user.successful_picks + 1)
                            if user.total_picks > 0:
                                CustomUser.objects.filter(id=user.id).update(success_rate=round(user.successful_picks/user.total_picks*100, 2))
                        
                        for pick in false_picks:
                            user = CustomUser.objects.get(id=pick.user_id)
                            if user.total_picks > 0:
                                CustomUser.objects.filter(id=user.id).update(success_rate=round(user.successful_picks/user.total_picks*100, 2))

                    except:
                        game_object.home_team = home_team
                        game_object.home_team_score = home_team_score
                        game_object.away_team = away_team
                        game_object.away_team_score = away_team_score
                        game_object.date = date
                        game_object.winner = winner
                        game_object.save()
                        Pick.objects.filter(game=game_object, team_picked=winner).update(successful_pick=True)
                        Pick.objects.filter(game=game_object, team_picked=loser).update(successful_pick=False)
                        correct_picks = Pick.objects.filter(game=game_object, successful_pick=True)
                        false_picks = Pick.objects.filter(game=game_object, successful_pick=False)
                        for pick in correct_picks:
                            user = CustomUser.objects.get(id=pick.user_id)
                            CustomUser.objects.filter(id=user.id).update(successful_picks= user.successful_picks + 1)
                            if user.total_picks > 0:
                                CustomUser.objects.filter(id=user.id).update(success_rate=round(user.successful_picks/user.total_picks*100, 2))

                        for pick in false_picks:
                            user = CustomUser.objects.get(id=pick.user_id)
                            if user.total_picks > 0:
                                CustomUser.objects.filter(id=user.id).update(success_rate=round(user.successful_picks/user.total_picks*100, 2))

        def scrape_upcoming_games():
            base_url = "https://www.nba.com/games?date="
            date_today = datetime.date.today()
            date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            dates = [date_today, date_tomorrow]
            for date in dates:
                url = base_url + str(date)
                driver = webdriver.Firefox()
                driver.get(url)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                games = soup.find_all("div", class_="GameCard_gc__UCI46 GameCardsMapper_gamecard__pz1rg")
                driver.close()

                for game in games:
                    game_object = Game()
                    team_names = game.find_all("span", class_="MatchupCardTeamName_teamName__9YaBA")
                    team_names_clean = [tag.get_text() for tag in team_names]
                    home_team_name = nba_teams.get(team_names_clean[1]) + " " + team_names_clean[1]
                    home_team = Team.objects.get(name=home_team_name)
                    away_team_name = nba_teams.get(team_names_clean[0]) + " " + team_names_clean[0]
                    away_team = Team.objects.get(name=away_team_name)

                    try:
                        game_check = Game.objects.get(home_team=home_team, away_team=away_team, date=date)

                    except:
                        game_object.home_team = home_team
                        game_object.away_team = away_team
                        game_object.date = date
                        game_object.save()


        scrape_past_games()
        scrape_upcoming_games()
                    
