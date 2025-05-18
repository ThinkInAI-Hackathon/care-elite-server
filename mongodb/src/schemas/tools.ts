import type { ListToolsRequest } from "@modelcontextprotocol/sdk/types.js";
import type { Db, MongoClient } from "mongodb";

export async function handleListToolsRequest({
  request,
  client,
  db,
  isReadOnlyMode,
}: {
  request: ListToolsRequest;
  client: MongoClient;
  db: Db;
  isReadOnlyMode: boolean;
}) {
  return {
    tools: [
      {
        name: "query",
        description:
          "Execute a MongoDB query with optional execution plan analysis",
        inputSchema: {
          type: "object",
          properties: {
            collection: {
              type: "string",
              description: "Name of the collection to query",
            },
            filter: { 
              type: "object", 
              description: "MongoDB query filter. Supports date strings in ISO format ('2025-01-01T00:00:00Z') and ISODate('2025-01-01T00:00:00Z') notation" 
            },
            projection: {
              type: "object",
              description: "Fields to include/exclude",
            },
            limit: {
              type: "number",
              description: "Maximum number of documents to return",
              default: 10,
            },
            explain: {
              type: "string",
              description: "Optional: Get query execution information",
              enum: ["queryPlanner", "executionStats", "allPlansExecution"],
            },
            objectIdMode: {
              type: "string",
              description: "Control how 24-character hex strings are handled",
              enum: ["auto", "none", "force"],
              default: "auto",
            },
          },
          required: ["collection"],
        },
      },
      {
        name: "aggregate",
        description:
          "Execute a MongoDB aggregation pipeline with optional execution plan analysis",
        inputSchema: {
          type: "object",
          properties: {
            collection: {
              type: "string",
              description: "Name of the collection to aggregate",
            },
            pipeline: {
              type: "array",
              description: "Aggregation pipeline stages. Supports date strings in ISO format ('2025-01-01T00:00:00Z') and ISODate('2025-01-01T00:00:00Z') notation",
              items: {
                type: "object",
              },
            },
            explain: {
              type: "string",
              description:
                "Optional: Get aggregation execution information (queryPlanner, executionStats, or allPlansExecution)",
              enum: ["queryPlanner", "executionStats", "allPlansExecution"],
            },
            objectIdMode: {
              type: "string",
              description: "Control how 24-character hex strings are handled",
              enum: ["auto", "none", "force"],
              default: "auto",
            },
          },
          required: ["collection", "pipeline"],
        },
      },
      {
        name: "update",
        description: "Update documents in a MongoDB collection",
        inputSchema: {
          type: "object",
          properties: {
            collection: {
              type: "string",
              description: "Name of the collection to update",
            },
            filter: {
              type: "object",
              description: "Filter to select documents to update. Supports date strings in ISO format ('2025-01-01T00:00:00Z') and ISODate('2025-01-01T00:00:00Z') notation",
            },
            update: {
              type: "object",
              description:
                "Update operations to apply ($set, $unset, $inc, etc.)",
            },
            upsert: {
              type: "boolean",
              description:
                "Create a new document if no documents match the filter",
            },
            multi: {
              type: "boolean",
              description: "Update multiple documents that match the filter",
            },
            objectIdMode: {
              type: "string",
              description: "Control how 24-character hex strings are handled",
              enum: ["auto", "none", "force"],
              default: "auto",
            },
          },
          required: ["collection", "filter", "update"],
        },
      },
      {
        name: "serverInfo",
        description:
          "Get MongoDB server information including version, storage engine, and other details",
        inputSchema: {
          type: "object",
          properties: {
            includeDebugInfo: {
              type: "boolean",
              description:
                "Include additional debug information about the server",
            },
          },
        },
      },
      {
        name: "insert",
        description: "Insert one or more documents into a MongoDB collection",
        inputSchema: {
          type: "object",
          properties: {
            collection: {
              type: "string",
              description: "Name of the collection to insert into",
            },
            documents: {
              type: "array",
              description: "Array of documents to insert",
              items: { type: "object" },
            },
            ordered: {
              type: "boolean",
              description:
                "If true, perform ordered insert. If false, insert unordered",
            },
            writeConcern: {
              type: "object",
              description: "Write concern for the insert operation",
            },
            bypassDocumentValidation: {
              type: "boolean",
              description: "Allow insert to bypass schema validation",
            },
            objectIdMode: {
              type: "string",
              description: "Control how 24-character hex strings are handled",
              enum: ["auto", "none", "force"],
              default: "auto",
            },
          },
          required: ["collection", "documents"],
        },
      },
      {
        name: "createIndex",
        description: "Create one or more indexes on a MongoDB collection",
        inputSchema: {
          type: "object",
          properties: {
            collection: {
              type: "string",
              description: "Name of the collection to create indexes on",
            },
            indexes: {
              type: "array",
              description: "Array of index specifications",
              items: {
                type: "object",
                properties: {
                  key: {
                    type: "object",
                    description: "Index key pattern, e.g. { field: 1 }",
                  },
                  name: {
                    type: "string",
                    description: "Optional: Name of the index",
                  },
                  unique: {
                    type: "boolean",
                    description: "Optional: Creates a unique index",
                  },
                  sparse: {
                    type: "boolean",
                    description: "Optional: Creates a sparse index",
                  },
                  background: {
                    type: "boolean",
                    description: "Optional: Builds index in background",
                  },
                  expireAfterSeconds: {
                    type: "number",
                    description: "TTL in seconds for documents",
                  },
                  partialFilterExpression: {
                    type: "object",
                    description: "Filter expression for partial indexes",
                  },
                },
                required: ["key"],
              },
            },
            writeConcern: {
              type: "object",
              description: "Write concern for index creation",
            },
            commitQuorum: {
              type: "string",
              description: "Number of members required to create the index",
            },
            objectIdMode: {
              type: "string",
              description: "Control how 24-character hex strings are handled",
              enum: ["auto", "none", "force"],
              default: "auto",
            },
          },
          required: ["collection", "indexes"],
        },
      },
      {
        name: "count",
        description: "Count documents in a collection matching a query",
        inputSchema: {
          type: "object",
          properties: {
            collection: { type: "string", description: "Collection name" },
            query: { type: "object", description: "Query filter to count" },
            limit: { type: "integer", description: "Max documents to count" },
            skip: {
              type: "integer",
              description: "Docs to skip before counting",
            },
            hint: { type: "object", description: "Index hint" },
            readConcern: { type: "object", description: "Read concern option" },
            maxTimeMS: { type: "integer", description: "Max execution time" },
            collation: {
              type: "object",
              description: "Collation rules for comparison",
            },
            objectIdMode: {
              type: "string",
              description: "Control how 24-character hex strings are handled",
              enum: ["auto", "none", "force"],
              default: "auto",
            },
          },
          required: ["collection"],
        },
      },
      {
        name: "listCollections",
        description: "List all collections in the MongoDB database",
        inputSchema: {
          type: "object",
          properties: {
            nameOnly: {
              type: "boolean",
              description: "If true, return only collection names",
            },
            filter: {
              type: "object",
              description: "Filter for collections",
            },
            objectIdMode: {
              type: "string",
              description: "Control how 24-character hex strings are handled",
              enum: ["auto", "none", "force"],
              default: "auto",
            },
          },
        },
      },
    ],
  };
}
