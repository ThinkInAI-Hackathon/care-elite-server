package main

import (
	"context"
	"eino_assistant/eino/rag"
	"fmt"
	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"os"
)

func main() {
	// 构建RAG系统
	ctx := context.Background()
	ragSystem, err := rag.BuildRAG(ctx, true, 3)
	if err != nil {
		fmt.Fprintf(os.Stderr, "构建RAG系统失败: %v\n", err)
		os.Exit(1)
	}

	// Create a new MCP server
	s := server.NewMCPServer(
		"Rag Demo",
		"1.0.0",
		server.WithToolCapabilities(false),
		server.WithRecovery(),
	)

	// Add a calculator tool
	calculatorTool := mcp.NewTool("care_elite_rag",
		mcp.WithDescription("月子中心智能专家系统"),
		mcp.WithString("question",
			mcp.Required(),
			mcp.Description("针对月子中心的各种场景的服务的使用资讯的rag系统"),
			mcp.Enum("我希望了解坐月子方式：家人照顾/顾月嫂/月子中心", "宝宝计划喂养方式：母乳喂养/喂奶粉", "对会所优势亮点没有观念"),
		),
	)

	// Add the calculator handler
	s.AddTool(calculatorTool, func(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		question := request.Params.Arguments["question"].(string)
		fmt.Println(question)
		//处理问题
		answer, err := ragSystem.Answer(ctx, question)
		if err != nil {
			fmt.Fprintf(os.Stderr, "处理问题时出错: %v\n", err)
			return nil, err
		}

		return mcp.NewToolResultText(fmt.Sprintf("%s", answer)), nil
	})

	// Start the server
	if err := server.ServeStdio(s); err != nil {
		fmt.Printf("Server error: %v\n", err)
	}
}
