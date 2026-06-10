import { Severity } from "../api";

const LABELS: Record<Severity, string> = {
  High: "High",
  Medium: "Medium",
  Low: "Low",
  Informational: "Info",
  Optimization: "Opt",
};

export default function SeverityBadge({ severity }: { severity: Severity }) {
  const cls = `badge badge-${severity.toLowerCase()}`;
  return <span className={cls}>{LABELS[severity]}</span>;
}
