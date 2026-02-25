export type GradeValue = "GREEN" | "GREEN_STAR" | "YELLOW" | "RED";

interface TrafficLightProps {
    grade: GradeValue | null;
    className?: string;
}

export function TrafficLight({ grade, className }: TrafficLightProps) {
    const bgColor = grade
        ? {
            GREEN: "bg-green-500",
            GREEN_STAR: "bg-green-500 ring-2 ring-green-300 ring-offset-1",
            YELLOW: "bg-yellow-500",
            RED: "bg-red-500",
        }[grade] || "bg-gray-300"
        : "bg-gray-300";

    return (
        <div
            className={["h-3 w-3 rounded-full flex-shrink-0", bgColor, className].filter(Boolean).join(" ")}
            title={grade || "Pending"}
        />
    );
}
