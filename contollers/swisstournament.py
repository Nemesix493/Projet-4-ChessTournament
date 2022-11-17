import math

import models


class SwissTournament:
    @staticmethod
    def max_rank_log10(players: list[models.Player]) -> int:
        """
        Return the ceil around log10 of the player with the highest rank to
        sort the players by score,rank
        :param players: list[models.Player]
        :return: int
        """
        ranks = [player.rank for player in players]
        ranks.sort(reverse=True)
        return math.ceil(math.log10(ranks[0]))

    @staticmethod
    def get_player_total_score(tournament: models.Tournament,
                               round_number: int | None = None) -> dict:
        """
        Return a dict where each key = player.pk and val = player_score
        :param tournament: models.Tournament
        :param round_number: int | None = None
        :return: dict
        """
        if round_number is None:
            round_number = len(tournament.rounds)
        players_total_score = {player.pk: 0 for player in tournament.players}
        for tournament_round in tournament.rounds[:round_number]:
            for match in tournament_round.matches:
                for line in match:
                    players_total_score[line[0].pk] += line[1]
        return players_total_score

    @staticmethod
    def first_round_peer(tournament: models.Tournament) -> models.Round:
        players = [player for player in tournament.players]
        players.sort(key=lambda player: player.rank, reverse=True)
        players_half_len = int(len(players)/2)
        tournament_round = models.Round()
        tournament_round.matches = [
            (
                [players[i], 0],
                [players[i + players_half_len], 0]
            )
            for i in range(players_half_len)
        ]
        return tournament_round

    @classmethod
    def next_round_peer(cls, tournament: models.Tournament) -> models.Round:
        players = [player for player in tournament.players]
        players_total_score = cls.get_player_total_score(tournament=tournament)
        score_factor = 10**cls.max_rank_log10(players)
        players.sort(
            key=lambda player:
            players_total_score[player.pk] * score_factor + player.rank,
            reverse=True
        )
        prepared_selection = cls.prepare_selection(
            players=players,
            tournament=tournament
        )
        tournament_round = models.Round()
        tournament_round.matches = []
        while len(prepared_selection) != 0:
            player_one = prepared_selection[0][0]
            player_two = prepared_selection[0][1][0]
            tournament_round.matches.append(
                (
                    [player_one, 0],
                    [player_two, 0]
                )
            )
            prepared_selection.pop(0)
            player_two_index = None
            for i in range(len(prepared_selection)):
                if prepared_selection[i][0] == player_two:
                    player_two_index = i
                else:
                    prepared_selection[i][1].remove(player_two)
                prepared_selection[i][1].remove(player_one)
            prepared_selection.pop(player_two_index)
        return tournament_round

    @classmethod
    def select_peer(cls, tournament: models.Tournament) -> models.Round:
        """
        Select the peer for a round and return the round
        :param tournament: models.Tournament
        :return: models.Round
        """
        if len(tournament.rounds) == 0:
            return cls.first_round_peer(tournament=tournament)
        else:
            return cls.next_round_peer(tournament=tournament)

    @staticmethod
    def calc_priority(player_tournament_rank: int,
                      players_number: int) -> list[int]:
        priorities = []
        for i in range(players_number - 1):
            if i % 2 == 0:
                priorities.append(
                    (player_tournament_rank + players_number // 2 - i // 2)
                    % players_number
                )
            else:
                priorities.append(
                    (
                        player_tournament_rank + players_number // 2 +
                        (i + 1) // 2
                    )
                    % players_number
                )
        return priorities

    @staticmethod
    def is_in_match(player: models.Player, match: tuple) -> bool:
        return match[0][0].pk == player.pk or match[1][0].pk == player.pk

    @classmethod
    def how_many_match_between(cls, tournament: models.Tournament,
                               player_one: models.Player,
                               player_two: models.Player) -> int:
        count = 0
        for tournament_round in tournament.rounds:
            for match in tournament_round.matches:
                if cls.is_in_match(player=player_one, match=match) and \
                        cls.is_in_match(player=player_two, match=match):
                    count += 1
                    break
                if cls.is_in_match(player=player_one, match=match) or \
                        cls.is_in_match(player=player_two, match=match):
                    break
        return count

    @classmethod
    def prepare_selection(cls, players: list[models.Player],
                          tournament: models.Tournament) -> list[tuple]:
        players_priorities = {
            players[i].pk:
                cls.calc_priority(
                    player_tournament_rank=i,
                    players_number=len(players)
                )
                for i in range(len(players))
        }
        players_opponents = [
            [player, [], [[] for i in range(len(tournament.rounds)+1)], '']
            for player in players
        ]
        for player_opponents in players_opponents:
            for priority in players_priorities[player_opponents[0].pk]:
                match_count = cls.how_many_match_between(
                    tournament=tournament,
                    player_one=player_opponents[0],
                    player_two=players[priority]
                )
                player_opponents[2][match_count].append(
                    players[priority]
                )
            for opponents in player_opponents[2]:
                for opponent in opponents:
                    player_opponents[1].append(opponent)
            # Making a string to sort the list
            for opponents in player_opponents[2]:
                player_opponents[3] += str(len(players) - len(opponents))
                player_opponents[3] += "0" * (
                    len(str(len(players))) -
                    len(str(len(players)-len(opponents)))
                )
        players_opponents.sort(key=lambda item: item[3], reverse=True)
        return [
            (player_opponents[0], player_opponents[1])
            for player_opponents in players_opponents
        ]
