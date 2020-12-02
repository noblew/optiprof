import React from 'react'

const CustomTooltip = ({ active, payload, label }) => {
    if (active) {
        const data = payload[0]['payload']
        return (
            <div className="custom-tooltip">
                <p className="label">
                    {data['department'] + ' ' + data['courseNumber'] + ': ' + data['courseName']}
                </p>
                {'semesterTerm' in data ? 
                    <p className="label">
                        Semester: {data['semesterTerm']}
                    </p> : null
                }
                <p className="label">Avg GPA: {data['avgGPA'].toFixed(2)}</p>
            </div>
        )
    }

    return null
}

export default CustomTooltip
