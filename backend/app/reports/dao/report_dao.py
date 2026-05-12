from sqlalchemy import text
from common.base_dao import BaseDao
from app.reports.model.report import Report
from core.db_postgres import AsyncSession
from datetime import date, timedelta

class ReportDao(BaseDao[Report]):
  NEGATIVE_DYNAMICS_COLOR = "red"
  POSITIVE_DYNAMICS_COLOR = "green"

  async def get_total_revenue(
    self,
    db: AsyncSession,
    date_from: date,
    date_to: date,
  ):
    """Получение отчета Выручка в месяц. Общая"""

    # async with async_session_maker() as session:
    query = text(
        f"""with sales as (
            select *, DATE_TRUNC('day', rd.moment) date
            from retail_demand rd
            where date_trunc('day',rd.moment) >=
            '{(date_from.replace(day=1) -
            timedelta(days=10)).replace(day=1)}'
            and date_trunc('day', rd.moment) <= '{date_to}'
            and applicable is true
        ), dates as (
            select *
            from generate_series(
                '{(date_from.replace(day=1) -
                timedelta(days=10)).replace(day=1)}'::timestamp,
                '{date_to.replace(day=1)}'::timestamp,
                '1 month'::interval
            ) date
        ), data as (
            select d.date, '' employee_name,
                case when count(s.id) > 0
                then sum(s.sum)
                else 0 end revenue
            from dates d
            left join sales s
            on d.date = DATE_TRUNC('month', s.date)
            group by d.date
        ) select d1.date, d1.employee_name,
            round(d1.revenue::numeric) revenue,
            case when d2.revenue > 0
            then round(
                ((d1.revenue /
                d2.revenue - 1) * 100)
            ::numeric) || '%'
            else null end revenue_dynamics,
            case when d1.revenue = 0.0
                and d2.revenue = 0.0
            then null
            when d1.revenue > d2.revenue
            then '{self.POSITIVE_DYNAMICS_COLOR}'
            else '{self.NEGATIVE_DYNAMICS_COLOR}'
            end color
        from data d1
        join data d2
        on d1.date = d2.date + interval '1 month'
        order by 1;
        """
    )

    result = await db.execute(query)
    return result.mappings().all()

  async def get_revenue(
    self,
    db: AsyncSession,
    date_from: date,
    date_to: date,
    retail_store_id: int,
  ):
    """Получение отчета Выручка в месяц"""
    # async with async_session_maker() as session:
    query = text(
        f"""with sales as (
            select *, DATE_TRUNC('day', rd.moment) date
            from retail_demand rd
            where date_trunc('day',rd.moment) >=
            '{(date_from.replace(day=1) -
            timedelta(days=10)).replace(day=1)}'
            and date_trunc('day', rd.moment) <= '{date_to}'
            and retail_store_id = '{retail_store_id}'
            and applicable is true
        ), users as (
            select *
            from "user" u
            where u.id in (select distinct owner_id from sales)
        ), dates as (
            select *
            from generate_series(
                '{(date_from.replace(day=1) -
                timedelta(days=10)).replace(day=1)}'::timestamp,
                '{date_to.replace(day=1)}'::timestamp,
                '1 month'::interval
            ) date
        ), data as (
            select d.date, u.name employee_name,
                case when count(s.id) > 0
                then sum(s.sum)
                else 0 end revenue
            from dates d
            cross join users u
            left join sales s
            on d.date = DATE_TRUNC('month', s.date)
            and u.id = s.owner_id
            group by d.date, u.name
                union all
            select d.date, '',
                case when count(s.id) > 0
                then sum(s.sum)
                else 0 end revenue
            from dates d
            cross join users u
            left join sales s
            on d.date = DATE_TRUNC('month', s.date)
            and u.id = s.owner_id
            group by d.date
        ) select d1.date, d1.employee_name,
            round(d1.revenue::numeric) revenue,
            case when d2.revenue > 0
            then round(
                ((d1.revenue /
                d2.revenue - 1) * 100)
            ::numeric) || '%'
            else null end revenue_dynamics,
            case when d1.revenue = 0.0
                and d2.revenue = 0.0
            then null
            when d1.revenue > d2.revenue
            then '{self.POSITIVE_DYNAMICS_COLOR}'
            else '{self.NEGATIVE_DYNAMICS_COLOR}'
            end color
        from data d1
        join data d2
        on d1.date = d2.date + interval '1 month'
        and d1.employee_name = d2.employee_name
        order by 2, 1;
        """
    )

    result = await db.execute(query)
    return result.mappings().all()
  
  async def get_shift_by_day(
    self,
    db: AsyncSession,
    date_from: date,
    date_to: date,
    retail_store_id: int,
  ):
    """Получение отчета Смены по дням"""
    query = text(
        f"""
        with sales as (
            select *, DATE_TRUNC('day', rd.moment) date
            from retail_demand rd
            where date_trunc('day',rd.moment) >= '{date_from}'
            and date_trunc('day',rd.moment) <= '{date_to}'
            and retail_store_id = '{retail_store_id}'
            and applicable is true
        ), users as (
            select *
            from "user" u
            where u.id in (select distinct owner_id from sales)
        ), dates as (
            select *
            from generate_series('{date_from}'::timestamp,
            '{date_to}'::timestamp, '1 day'::interval) date
        ) select d.date, u.name employee_name, case when count(s.id) > 0
        then 1 else 0 end  shift_count
        from dates d
        cross join users u
        left join sales s
        on s.owner_id = u.id
        and d.date = s.date
        group by d.date, u.name
        order by u.name, d.date"""
    )

    result = await db.execute(query)
    return result
  
  async def get_shift_by_month(
    self,
    db: AsyncSession,
    date_from: date,
    date_to: date,
    retail_store_id: int,
  ):
    """Получение отчета Смены по месяцам"""
    query = text(
        f"""
        with sales as (
            select *, DATE_TRUNC('day', rd.moment) date
            from retail_demand rd
            where date_trunc('day',rd.moment) >= '{date_from}'
            and date_trunc('day',rd.moment) <= '{date_to}'
            and retail_store_id = '{retail_store_id}'
            and applicable is true
        ), users as (
            select *
            from "user" u
            where u.id in (select distinct owner_id from sales)
        ), dates as (
            select *
            from generate_series('{date_from}'::timestamp,
            '{date_to}'::timestamp, '1 day'::interval) date
        ), shift_on_day as (
        select d.date, u.name employee_name, case when count(s.id) > 0
        then 1 else 0 end  shift_count
            from dates d
            cross join users u
            left join sales s
            on s.owner_id = u.id
            and d.date = s.date
            group by d.date, u.name
        ) select date_trunc('month', date) date, employee_name,
        sum(shift_on_day.shift_count) shift_count
        from shift_on_day
        group by date_trunc('month', date), employee_name
        order by employee_name, date
    """
    )

    result = await db.execute(query)
    return result

report_dao: ReportDao = ReportDao(Report)