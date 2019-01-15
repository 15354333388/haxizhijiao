from django.contrib import admin
from  . import models
# Register your models here.

admin.site.register([models.User, models.Manoeuvre, models.ManoeuverMiddle, models.Work,
                     models.WorkMiddle, models.Examine, models.ExamineMiddle, models.Train,
                     models.TrainMiddle,models.Incident])
