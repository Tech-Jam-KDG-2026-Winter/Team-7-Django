from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from tasks.models import TaskDailyAchieved
import calendar

# Create your views here.
class CalendarView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        
        today = timezone.now().date()
        try:
            year = int(request.GET.get('year', today.year))
            month = int(request.GET.get('month', today.month))
        except ValueError:
            year = today.year
            month = today.month

        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdatescalendar(year, month)

        start_date = month_days[0][0] 
        end_date = month_days[-1][-1] 

        # 期間内の達成タスクを取得
        achieved_tasks = TaskDailyAchieved.objects.filter(
            user_id=user_id,
            created_at__range=[start_date, end_date]
        ).select_related('task')

        # 日付ごとのカロリーを集計
        daily_calories = {}
        for achievement in achieved_tasks:
            date_key = achievement.created_at
            if date_key not in daily_calories:
                daily_calories[date_key] = 0
            daily_calories[date_key] += achievement.task.calorie

        # カレンダー表示用のデータ構築
        calendar_data = []
        for week in month_days:
            week_data = []
            for day in week:
                is_current_month = (day.month == month)
                calories = daily_calories.get(day, 0)
                week_data.append({
                    'date': day,
                    'day': day.day,
                    'is_current_month': is_current_month,
                    'calories': calories
                })
            calendar_data.append(week_data)

        prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
        next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

        context = {
            'calendar_data': calendar_data,
            'year': year,
            'month': month,
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
        }

        return render(request, 'calendar.html', context)
