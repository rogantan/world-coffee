import calendar
from sqlalchemy import text
from core.db_postgres import AsyncSession
from datetime import date, timedelta

class DashboardDao:
    async def get_revenue_dynamics(
        self,
        db: AsyncSession,
        report_title: str,
        month_start: date
    ):
        """Показатель выручки"""
        # Вычисляем даты заранее
        current_month_start = month_start.replace(day=1)
        last_month_start = (month_start.replace(day=1) - timedelta(days=1)).replace(day=1)

        query = text(
            """
            with 
            current_month_revenue as (
                select sum(rd.sum) revenue
                from retail_demand rd
                join retail_store rs on rs.id = rd.retail_store_id
                where date_trunc('month', rd.moment) = :current_month_start
                and rs.name = :report_title
                and rd.applicable is true
            ), 
            last_month_revenue as (
                select sum(rd.sum) revenue
                from retail_demand rd
                join retail_store rs on rs.id = rd.retail_store_id
                where date_trunc('month', rd.moment) = :last_month_start
                and rs.name = :report_title
                and rd.applicable is true
            ) 
            select 'р.' || coalesce(round(lm.revenue::numeric, 2), 0) as last_month,
                   'р.' || coalesce(round(cm.revenue::numeric, 2), 0) as current_month,
                   case when lm.revenue > 0
                   then round(((coalesce(cm.revenue, 0)::numeric / lm.revenue - 1) * 100)::numeric, 2) || '%' 
                   else '0%' end as lfl
            from last_month_revenue lm, current_month_revenue cm
            """
        )
        
        result = await db.execute(
            query, 
            {
                "report_title": report_title,
                "current_month_start": current_month_start,
                "last_month_start": last_month_start
            }
        )
        return result.mappings().first()
    
    async def get_average_daily_revenue_dynamics(
        self,
        db: AsyncSession,
        report_title: str,
        month_start: date,
    ):
        """Показатель средней выручки за день"""

        today = date.today()
        if today.month == month_start.month and today.year == month_start.year:
            days_in_month = today.day
        else:
            days_in_month = calendar.monthrange(month_start.year, month_start.month)[1]

        query = text(
            f"""with 
            current_month_revenue as (
                select sum(sum) / {days_in_month} revenue 
                from (select sum(sum) sum
                    from retail_demand rd
                    join retail_store rs on rs.id = rd.retail_store_id
                    where date_trunc('month',rd.moment) = '{month_start.replace(day=1)}'
                    and rs.name = '{report_title}'
                    and applicable is true
                    group by date_trunc('day', moment)
                    ) as daily_revenue
            ), 
            last_month_revenue as (
                select sum(sum) / {calendar.monthrange(month_start.year, month_start.month)[1]} revenue
                from (select sum(sum) sum
                    from retail_demand rd
                    join retail_store rs on rs.id = rd.retail_store_id
                    where date_trunc('month',rd.moment) =
                    '{(month_start.replace(day=1) -
                    timedelta(days=1)).replace(day=1)}'
                    and rs.name = '{report_title}'
                    and applicable is true
                    group by date_trunc('day', moment)
                    ) as daily_revenue
            ) select 'р.' || coalesce(round(lm.revenue::numeric, 2), 0) last_month,
                    'р.' || coalesce(round(cm.revenue::numeric, 2), 0) current_month,
                    case when lm.revenue > 0
                    then round(((coalesce(cm.revenue, 0)::numeric / lm.revenue - 1) * 100)::numeric, 2) || '%' 
                    else '0%' end lfl
                from last_month_revenue lm, current_month_revenue cm
            """
        )

        result = await db.execute(query)
        return result.mappings().first()
    
    async def get_number_of_checks_dynamics(
        self,
        db: AsyncSession,
        report_title: str,
        month_start: date,
    ):
        query = text(
            f"""with 
            current_month_number_of_checks as (
                select count(*) number_of_checks
                from retail_demand rd
                join retail_store rs on rs.id = rd.retail_store_id
                where date_trunc('month',rd.moment) = '{month_start.replace(day=1)}'
                and rs.name = '{report_title}'
                and applicable is true
            ), 
            last_month_number_of_checks as (
                select count(*) number_of_checks
                from retail_demand rd
                join retail_store rs on rs.id = rd.retail_store_id
                where date_trunc('month',rd.moment) =
                '{(month_start.replace(day=1) -
                timedelta(days=1)).replace(day=1)}'
                and rs.name = '{report_title}'
                and applicable is true
            ) select coalesce(lm.number_of_checks, 0) last_month,
                    coalesce(cm.number_of_checks, 0) current_month,
                    case when lm.number_of_checks > 0
                    then round(((coalesce(cm.number_of_checks, 0)::numeric / lm.number_of_checks - 1) * 100)::numeric, 2) || '%' 
                    else '0%' end lfl
                from last_month_number_of_checks lm, current_month_number_of_checks cm
            """
        )

        result = await db.execute(query)
        return result.mappings().first()
    
    async def get_average_number_of_checks_dynamics(
        self,
        db: AsyncSession,
        report_title: str,
        month_start: date,
    ):
        today = date.today()
        if today.month == month_start.month and today.year == month_start.year:
            days_in_month = today.day
        else:
            days_in_month = calendar.monthrange(month_start.year, month_start.month)[1]

        query = text(
            f"""with current_month_number_of_checks as (
                select sum(count) / {days_in_month} number_of_checks 
                from (select count(*) count
                    from retail_demand rd
                    join retail_store rs on rs.id = rd.retail_store_id
                    where date_trunc('month',rd.moment) = '{month_start.replace(day=1)}'
                    and rs.name = '{report_title}'
                    and applicable is true
                    group by date_trunc('day', moment)
                    ) as daily_number_of_checks
            ), last_month_number_of_checks as (
                select sum(count) / {calendar.monthrange(month_start.year, month_start.month)[1]} number_of_checks
                from (select count(*) count
                    from retail_demand rd
                    join retail_store rs on rs.id = rd.retail_store_id
                    where date_trunc('month',rd.moment) =
                    '{(month_start.replace(day=1) -
                    timedelta(days=1)).replace(day=1)}'
                    and rs.name = '{report_title}'
                    and applicable is true
                    group by date_trunc('day', moment)
                    ) as daily_number_of_checks
            ) select 
                    coalesce(round(lm.number_of_checks, 1), 0) last_month,
                    coalesce(round(cm.number_of_checks, 1), 0) current_month,
                    case when lm.number_of_checks > 0
                    then round(((coalesce(cm.number_of_checks, 0)::numeric / lm.number_of_checks - 1) * 100)::numeric, 2) || '%' 
                    else '0%' end lfl
                from last_month_number_of_checks lm, current_month_number_of_checks cm
            """
        )

        result = await db.execute(query)
        return result.mappings().first()
    
    async def get_average_check_dynamics(
        self,
        db: AsyncSession,
        report_title: str,
        month_start: date,
    ):
        query = text(
            f"""with 
            current_month_avg_check as (
                select avg(sum) avg_check
                from retail_demand rd
                join retail_store rs on rs.id = rd.retail_store_id
                where date_trunc('month',rd.moment) = '{month_start.replace(day=1)}'
                and rs.name = '{report_title}'
                and applicable is true
            ), 
            last_month_avg_check as (
                select avg(sum) avg_check
                from retail_demand rd
                join retail_store rs on rs.id = rd.retail_store_id
                where date_trunc('month',rd.moment) =
                '{(month_start.replace(day=1) -
                timedelta(days=1)).replace(day=1)}'
                and rs.name = '{report_title}'
                and applicable is true
            ) select 'р.' || coalesce(round(lm.avg_check::numeric, 2), 0) last_month,
                    'р.' || coalesce(round(cm.avg_check::numeric, 2), 0) current_month,
                    case when lm.avg_check > 0
                    then round(((coalesce(cm.avg_check, 0)::numeric / lm.avg_check - 1) * 100)::numeric, 2) || '%' 
                    else '0%' end lfl
                from last_month_avg_check lm, current_month_avg_check cm
            """
        )

        result = await db.execute(query)
        return result.mappings().first()


dashboard_dao: DashboardDao = DashboardDao()