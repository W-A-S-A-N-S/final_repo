from django.db import models
from django.conf import settings
from places.models import Place  # places 앱의 Place 모델 참조

class TravelPlan(models.Model):
    """
    여행 일정 (travel_plans)
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    class PlanType(models.TextChoices):
        PERSONAL = 'personal', 'Personal'
        AI_RECOMMENDED = 'ai_recommended', 'AI Recommended'
        
    plan_type = models.CharField(max_length=20, choices=PlanType.choices, default=PlanType.PERSONAL)
    ai_prompt = models.TextField(blank=True, null=True)
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    is_public = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'travel_plans'
        # SQL 파일의 INDEX 반영
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_public']),
            models.Index(fields=['user', 'is_public']), # 복합 인덱스
        ]

class PlanDetail(models.Model):
    """
    일정 상세 (plan_details)
    """
    plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='details')
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    order_index = models.IntegerField(default=0)
    
    # DB에 없는 장소(임시 장소) 처리
    temp_place_name = models.CharField(max_length=255, blank=True, null=True)
    temp_place_address = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'plan_details'
        ordering = ['date', 'order_index']
        indexes = [
            models.Index(fields=['plan']),
            models.Index(fields=['date']),
            models.Index(fields=['place']),
        ]

class TravelPost(models.Model):
    """
    여행기 게시글 (travel_posts)
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(TravelPlan, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail_url = models.CharField(max_length=500, blank=True, null=True)
    
    # ★ 추가된 필드 (SQL 반영)
    destination = models.CharField(max_length=100, blank=True, null=True, help_text="여행지 (예: 서울, 부산)")
    is_public = models.BooleanField(default=True)
    
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'travel_posts'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['plan']),
            models.Index(fields=['created_at']),
            models.Index(fields=['like_count']), # 인기순 정렬용
            models.Index(fields=['-like_count', '-created_at']), # 복합 정렬 최적화
            models.Index(fields=['destination']), # 지역별 검색용
            models.Index(fields=['-view_count']), # 조회수 정렬용
        ]

class PostLike(models.Model):
    """
    게시글 좋아요 (post_likes)
    """
    post = models.ForeignKey(TravelPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_likes'
        unique_together = ('post', 'user') # 중복 좋아요 방지 (PK 대체)
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

class Comment(models.Model):
    """
    댓글 (comments) - Soft Delete 반영
    """
    post = models.ForeignKey(TravelPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    content = models.TextField()
    
    # ★ Soft Delete 필드 (SQL 반영)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['parent_comment']),
        ]