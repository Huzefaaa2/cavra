param location string = resourceGroup().location
param namePrefix string = 'cavra-zt'
param cavraApiImage string
param scannerImage string = 'python:3.12-slim'
param tenantId string
param workspaceId string
param externalIngress bool = false

resource log 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${namePrefix}-law'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource env 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: '${namePrefix}-env'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: log.properties.customerId
        sharedKey: log.listKeys().primarySharedKey
      }
    }
  }
}

resource cavraApi 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${namePrefix}-cavra-api'
  location: location
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      ingress: {
        external: externalIngress
        targetPort: 8000
      }
    }
    template: {
      containers: [
        {
          name: 'cavra-api'
          image: cavraApiImage
          env: [
            { name: 'CAVRA_FAIL_CLOSED', value: 'true' }
            { name: 'CAVRA_TENANT_ID', value: tenantId }
            { name: 'CAVRA_WORKSPACE_ID', value: workspaceId }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
}

resource cavraScanner 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${namePrefix}-cavra-scanner'
  location: location
  properties: {
    managedEnvironmentId: env.id
    template: {
      containers: [
        {
          name: 'cavra-scanner'
          image: scannerImage
          env: [
            { name: 'CAVRA_SCANNER_MODE', value: 'metadata_only' }
            { name: 'CAVRA_FAIL_CLOSED', value: 'true' }
            { name: 'CAVRA_TENANT_ID', value: tenantId }
            { name: 'CAVRA_WORKSPACE_ID', value: workspaceId }
          ]
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 1
      }
    }
  }
}

output apiName string = cavraApi.name
output scannerName string = cavraScanner.name
