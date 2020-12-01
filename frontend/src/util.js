function vizDataHandler(resultData, criteria) {
    let vizDict = {}
    for (let i = 0; i < resultData.length; i++) {
        if (criteria === 'department') {
            // no need to edit; resultData is a list of dictionaries to create a scatterplot
            return resultData
        } else if (criteria === 'course') {
            // no need to change; resultData is a list of dictionaries to create scatterplot
            return resultData
        } else {
            // professor
            let key = resultData[i]['department'] + ' ' + resultData[i]['courseNumber'].toString(10)
            if (!(key in vizDict)) {
                vizDict[key] = []
            } else {
                vizDict[key].push(resultData[i])
            }
        }
    }

    // sort the dictionary by semester
    let final_keys = Object.keys(vizDict)
    for (let i = 0; i < final_keys.length; i++) {
        vizDict[final_keys[i]].sort(sortSemTerm)
    }
    
    return vizDict
}

function sortSemTerm(x, y) {
    // x and y are objects
    const splitx = x['semesterTerm'].split("-")
    const splity = y['semesterTerm'].split("-")

    if (parseInt(splitx[0], 10) < parseInt(splity[0], 10)) {
        return -1
    } else if (parseInt(splitx[0], 10) > parseInt(splity[0], 10)) {
        return 1
    } else {
        if (splitx[1] === 'fa' && (splity[1] === 'su' || splity[1] === 'sp')) {
            return 1
        } else if (splitx[1] === 'sp' && (splity[1] === 'su' || splity[1] === 'fa')) {
            return -1
        } else if (splitx[1] === 'su' && splity[1] === 'fa') {
            return -1
        } else if (splitx[1] === 'su' && splity[1] === 'sp') {
            return 1
        }
        
        return 0
    }
}

export {
    vizDataHandler
}