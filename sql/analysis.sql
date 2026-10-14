-- Portfolio scenarios only. No actual customer support or production SLA data.

-- Queue and resolution metrics by category.
SELECT category, COUNT(*) AS tickets,
       ROUND(AVG(minutes_to_resolve), 1) AS mean_resolution_minutes,
       SUM(reopened) AS reopened_tickets,
       SUM(escalated) AS escalated_tickets
FROM tickets GROUP BY category ORDER BY tickets DESC;

-- Fictional assets that need patch or encryption review.
SELECT asset_tag, asset_type, status, encryption_status, patch_state, last_inventory_check
FROM assets
WHERE patch_state <> 'Current' OR encryption_status = 'Needs review'
ORDER BY last_inventory_check;

-- Lifecycle items blocked on approval, data retention, or access owner.
SELECT request_id, request_type, effective_date, manager_approval,
       access_review, data_retention, status
FROM lifecycle
WHERE lower(manager_approval) <> 'approved'
   OR lower(access_review) LIKE '%pending%'
   OR lower(data_retention) LIKE '%pending%'
ORDER BY effective_date;

-- Inventory reconciliation: assets with associated tickets versus total register.
SELECT COUNT(DISTINCT a.asset_tag) AS assets_with_tickets,
       (SELECT COUNT(*) FROM assets) AS total_assets
FROM assets a JOIN tickets t USING (asset_tag);
