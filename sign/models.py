from django.db import models

# Create your models here.
#发布会表
class Event(models.Model):
        name = models.CharField(max_length=100)  # 发布会标题
        limit = models.IntegerField()  # 参加人数
        status = models.BooleanField()  # 状态
        address = models.CharField(max_length=200)  # 地址
        start_time = models.DateTimeField('events time')  # 发布会时间
        create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

        def __str__(self):
            return self.name  # 将类实例/类对象以str形式显示。如：有一个类实例P，print P会显示为该实例的name

class Guest(models.Model):
    event=models.ForeignKey(Event)                  # 关联发布会，访问该属性直接显示对应的event.name，由event_id关联
    realname=models.CharField(max_length=64)        # 姓名
    phone=models.CharField(max_length=16)           # 手机号
    email=models.EmailField()                       # 邮箱
    sign=models.BooleanField()                      # 签到状态
    create_time=models.DateTimeField(auto_now=True) # 创建时间（自动获取当前时间）

    class Meta:
        unique_together=('event','phone')

    def __str__(self):
        return self.realname