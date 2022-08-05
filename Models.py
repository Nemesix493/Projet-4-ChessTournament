import models


class Round(models.Model):
    pass


class Player(models.Model):
    pass


class Tournament(models.Model):
    name = models.StringField()
    place = models.StringField()
    round_number = models.IntField(default=4)
    tour = models.ForeignKey(field_type=Round)
    player = models.ForeignKey(field_type=Player)

models.init_models(mod=__name__)