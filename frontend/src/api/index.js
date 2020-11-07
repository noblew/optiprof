function getApiEndpoint() {
    if (process.env.NODE_ENV === "prod") {
      // If API endpoint is specified in an environment variable with production deployment
      return process.env.PROF_API_ENDPOINT;
    } else {
      // Otherwise, use development endpoint
      return "http://localhost:5000";
    }
}

async function requestWrapper({
    path,
    method = "GET",
    data = null
  }) {
    let headers = {};
    if (data != null) {
      headers["Content-Type"] = "application/json";
    }
    
    const response = await fetch(
      `${getApiEndpoint()}${path}`, 
      {
        method,
        headers,
        body: data ? JSON.stringify(data) : null
      }
    );
  
    return {
      success: response.ok,
      data: await response.json()
    };
  }

const apiWrapper = {
    async testMethod() {
        return requestWrapper({
          path: '/',
          method: "GET"
        })
    },

    async insertRecord(data) {
        return requestWrapper({
            path: '/insert',
            method: 'POST',
            data: data
        })
    },

    async updateRecord(data) {
        return requestWrapper({
            path: '/update',
            method: 'PUT',
            data: data
        })
    },

    async deleteRecord(data) {
        return requestWrapper({
            path: '/delete',
            method: 'DELETE',
            data:{ "recordId": data}
        })
    },

    async searchRecords(input) {
        return requestWrapper({
            path: '/search/' + input,
            method: 'GET'
        })
    }
}

export default apiWrapper