USE [healthcare_analytics]
GO

/****** Object:  View [dbo].[vw_monthly_revenue]    Script Date: 29-01-2026 16:56:32 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE   VIEW [dbo].[vw_monthly_revenue] AS
SELECT
    FORMAT(d.date_key, 'yyyy-MM') AS year_month,
    SUM(fc.claim_amount) AS total_billed,
    SUM(fc.paid_amount) AS total_paid,
    SUM(fc.unpaid_amount) AS total_unpaid,
    CAST(SUM(fc.paid_amount) * 1.0 / NULLIF(SUM(fc.claim_amount), 0) AS DECIMAL(10,4)) AS collection_rate
FROM dbo.fact_claims fc
JOIN dbo.dim_date d
    ON d.date_key = fc.visit_date_key
GROUP BY FORMAT(d.date_key, 'yyyy-MM');
GO


USE [healthcare_analytics]
GO

/****** Object:  View [dbo].[vw_denial_rate_by_payer]    Script Date: 29-01-2026 16:56:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE   VIEW [dbo].[vw_denial_rate_by_payer] AS
SELECT
    payer,
    COUNT(*) AS total_claims,
    SUM(is_denied) AS denied_claims,
    CAST(SUM(is_denied) * 1.0 / NULLIF(COUNT(*), 0) AS DECIMAL(10,4)) AS denial_rate,
    SUM(unpaid_amount) AS total_unpaid_amount
FROM dbo.fact_claims
GROUP BY payer;
GO



USE [healthcare_analytics]
GO

/****** Object:  View [dbo].[vw_days_to_payment_trend]    Script Date: 29-01-2026 16:55:29 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE   VIEW [dbo].[vw_days_to_payment_trend] AS
SELECT
    FORMAT(d.date_key, 'yyyy-MM') AS year_month,
    AVG(CAST(fc.days_to_payment AS FLOAT)) AS avg_days_to_payment,
    COUNT(*) AS paid_claims
FROM dbo.fact_claims fc
JOIN dbo.dim_date d
    ON d.date_key = fc.visit_date_key
WHERE fc.claim_status = 'Paid'
GROUP BY FORMAT(d.date_key, 'yyyy-MM');
GO


