module MessageRetentionGuardian
  SAMPLE_DATA = {
    dashboard: {
      active_policies: 5,
      legal_holds: 3,
      deletion_windows: 11,
      urgent_risks: 2
    },
    policies: [
      {
        id: "policy-slack-finance",
        name: "Finance Slack retention",
        surface: "Slack",
        owner: "Records Management",
        retention_days: 2555,
        legal_hold: true,
        deletion_mode: "frozen",
        pressure: "high"
      },
      {
        id: "policy-email-hr",
        name: "HR mailbox retention",
        surface: "Exchange",
        owner: "HR Systems",
        retention_days: 2190,
        legal_hold: false,
        deletion_mode: "scheduled",
        pressure: "watch"
      },
      {
        id: "policy-chat-support",
        name: "Support chat retention",
        surface: "Zendesk Chat",
        owner: "Support Operations",
        retention_days: 365,
        legal_hold: false,
        deletion_mode: "scheduled",
        pressure: "stable"
      }
    ],
    requests: [
      {
        id: "request-7801",
        surface: "Slack",
        team: "Finance",
        hold_scope: "Acquisition diligence",
        retention_gap_days: 14,
        pending_deletions: 1882,
        export_backlog: 6,
        shadow_channels: 4,
        region_mismatch: true,
        pressure: "critical"
      },
      {
        id: "request-7814",
        surface: "Exchange",
        team: "HR",
        hold_scope: "Regional labor inquiry",
        retention_gap_days: 2,
        pending_deletions: 212,
        export_backlog: 1,
        shadow_channels: 0,
        region_mismatch: false,
        pressure: "watch"
      },
      {
        id: "request-7833",
        surface: "Zendesk Chat",
        team: "Support",
        hold_scope: "Standard retention run",
        retention_gap_days: 0,
        pending_deletions: 45,
        export_backlog: 0,
        shadow_channels: 0,
        region_mismatch: false,
        pressure: "stable"
      }
    ]
  }.freeze
end

