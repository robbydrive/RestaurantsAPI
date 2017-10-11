# Restaurants API
### Intended usage
This project can be a starting point for restaurants that wish to automate processes at place.
### API
There are 2 functions API can handle at the moment: providing full menu and creating new clients' orders. Available at `/api/`.
#### Authorization
Django OAuth Toolkit is used for authentication and authorization of API users.
Supposed workflow (examples in cURL):
1. Register new application that uses API to obtain application-specific client id and client secret (request it from admin).
2. Request token (with your user credentials):  
` curl -v -u $CLIENT_ID:$CLIENT_SECRET --data-urlencode "grant_type=password" --data-urlencode "username=$USERNAME" --data-urlencode "password=$PASSWORD" https://$YOUR_HOST/o/token/ `  
Response:  
> {"access_token": "HvtPEs0j6Nmv3hasvDLEueAUJlPYfO", "expires_in": 36000, "token_type": "Bearer", "scope": "read write", "refresh_token": "L4DYFWX393ifscxW8XSqRX4zkwduMx"}

#### Requests
Use access_token from previous section to make available requests to API.  
Example:  
`curl -v -H "Authorization: Bearer $TOKEN" https://$YOUR_HOST/api/categories/`  
Response:  
> {"data": [{"id": 1, "name": "Category 1", "type": "categories", "children": []}], "message": "Success"}

### Management tool
Web application for restaurants administrators allowing to change presented menu and orders status. Available at `/management/`.
