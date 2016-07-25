from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


from bbapp.scripts.getScores import doScoresScrape, fixScores

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/10')),
    name="scrape_espn_feed",
    ignore_result=True
)
def scrape_espn_feed():
    """
    Saves latest image from Flickr
    """
    thescores = doScoresScrape()
    fixScores(thescores, 'MLB')
    logger.info("Scores scraped")