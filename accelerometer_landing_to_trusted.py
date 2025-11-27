import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Customer Trusted
CustomerTrusted_node1763643612782 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_trusted", transformation_ctx="CustomerTrusted_node1763643612782")

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1764272553217 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://stedi-lake-house/accelerometer/landing/"], "recurse": True}, transformation_ctx="AccelerometerLanding_node1764272553217")

# Script generated for node Join
Join_node1763643636093 = Join.apply(frame1=CustomerTrusted_node1763643612782, frame2=AccelerometerLanding_node1764272553217, keys1=["email"], keys2=["user"], transformation_ctx="Join_node1763643636093")

# Script generated for node Privacy filter
SqlQuery0 = '''
select * from myDataSource
where timestamp >= shareWithResearchAsOfDate;
'''
Privacyfilter_node1763643992315 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":Join_node1763643636093}, transformation_ctx = "Privacyfilter_node1763643992315")

# Script generated for node Drop Fields
DropFields_node1763644123709 = DropFields.apply(frame=Privacyfilter_node1763643992315, paths=["birthDay", "shareWithPublicAsOfDate", "shareWithResearchAsOfDate", "registrationDate", "customerName", "shareWithFriendsAsOfDate", "email", "lastUpdateDate", "phone", "serialNumber"], transformation_ctx="DropFields_node1763644123709")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=DropFields_node1763644123709, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1763643375558", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1763644235527 = glueContext.getSink(path="s3://stedi-lake-house/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1763644235527")
AmazonS3_node1763644235527.setCatalogInfo(catalogDatabase="stedi",catalogTableName="accelerometer_trusted")
AmazonS3_node1763644235527.setFormat("json")
AmazonS3_node1763644235527.writeFrame(DropFields_node1763644123709)
job.commit()
