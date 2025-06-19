from tools import dijkstra
import json
import tkinter as tk
from tkinter import ttk, scrolledtext

def search_routes():
    # 우선순위 정의
    priorities = {
        '최소 시간순': 'time',
        '최소 비용순': 'cost',
        '최소 탄소 배출순': 'carbon',
        '최소 환적순': 'transfers'
    }

    # 결과 영역 초기화
    result_text.delete(1.0, tk.END)
    
    # 사용자 입력 가져오기
    start = start_var.get()
    end = end_var.get()
    selected_priority = priority_var.get()
    
    # 상태 업데이트
    status_var.set(f"경로 검색 중: {start} → {end} ({selected_priority})")
    root.update()
    
    # 제목 표시
    result_text.insert(tk.END, f"--- 출발: {start}, 도착: {end} 경로 검색 ({selected_priority}) ---\n")
    result_text.insert(tk.END, "-" * 40 + "\n\n")
    
    # 선택된 우선순위만 처리
    if selected_priority == '모든 경로':
        # 모든 우선순위에 대해 경로 계산
        results = {}
        for name, key in priorities.items():
            result = dijkstra(graph, start, end, key)
            if result == "No path found":
                result_text.insert(tk.END, "경로를 찾을 수 없습니다.\n")
                status_var.set("검색 완료: 결과 없음")
                return
            elif result == "Same node":
                result_text.insert(tk.END, "출발지와 도착지가 동일합니다.\n")
                status_var.set("검색 완료: 동일 노드")
                return
            results[name] = result
    else:
        # 선택된 우선순위에 대해서만 경로 계산
        key = priorities[selected_priority]
        result = dijkstra(graph, start, end, key)
        if result == "No path found":
            result_text.insert(tk.END, "경로를 찾을 수 없습니다.\n")
            status_var.set("검색 완료: 결과 없음")
            return
        elif result == "Same node":
            result_text.insert(tk.END, "출발지와 도착지가 동일합니다.\n")
            status_var.set("검색 완료: 동일 노드")
            return
        results = {selected_priority: result}
    
    # 결과 출력
    for name, data in results.items():
        days = data['time'] / 24
        
        result_text.insert(tk.END, f"\n⭐ {name} ⭐\n")
        
        # 경로 정보
        path_str = " → ".join([p['to'] for p in data['path_details']])
        result_text.insert(tk.END, f"  - 경로: {data['path_details'][0]['from']} → {path_str}\n")
        
        # 시간, 비용, 탄소 등
        result_text.insert(tk.END, f"  - 총 소요 시간: {days:.1f}일 ({data['time']}시간)\n")
        result_text.insert(tk.END, f"  - 총 비용: ${data['cost']:,}\n")
        result_text.insert(tk.END, f"  - 총 탄소 배출량: {data['carbon']:,} kg CO2e\n")
        result_text.insert(tk.END, f"  - 환적 횟수: {data['transfers']}회\n")
        result_text.insert(tk.END, "-" * 40 + "\n")
    
    status_var.set("검색 완료")


if __name__ == '__main__':
    # 그래프 로드
    with open('graph.json', 'r', encoding='utf-8') as f:
        graph = json.load(f)
    
    # Tkinter 윈도우 생성
    root = tk.Tk()
    root.title("물류 경로 검색")
    root.geometry("650x450")  # 창 크기 약간 늘림
    
    # 변수 초기화
    start_var = tk.StringVar()
    end_var = tk.StringVar()
    priority_var = tk.StringVar(value="모든 경로")
    status_var = tk.StringVar(value="준비됨")
    nodes = list(graph.keys())
    
    # 입력 프레임
    input_frame = tk.Frame(root, padx=10, pady=10)
    input_frame.pack(fill="x")
    
    # 출발지/도착지/우선순위 선택 영역
    tk.Label(input_frame, text="출발지:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    start_combo = ttk.Combobox(input_frame, textvariable=start_var, values=nodes, width=15)
    start_combo.current(0)
    start_combo.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(input_frame, text="도착지:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    end_combo = ttk.Combobox(input_frame, textvariable=end_var, values=nodes, width=15)
    end_combo.current(len(nodes)-1)  # 마지막 노드 선택 (보통 목적지)
    end_combo.grid(row=0, column=3, padx=5, pady=5)
    
    # 우선순위 선택 드롭다운 추가
    tk.Label(input_frame, text="우선순위:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    priority_options = ["모든 경로", "최소 시간순", "최소 비용순", "최소 탄소 배출순", "최소 환적순"]
    priority_combo = ttk.Combobox(input_frame, textvariable=priority_var, values=priority_options, width=15)
    priority_combo.current(0)  # 기본값 "모든 경로"
    priority_combo.grid(row=1, column=1, padx=5, pady=5)
    
    # 검색 버튼
    search_button = tk.Button(input_frame, text="경로 검색", command=search_routes,
                              bg="#4285f4", fg="white", padx=10)
    search_button.grid(row=2, column=0, columnspan=4, pady=10)
    
    # 결과 표시 영역
    result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15)
    result_text.pack(fill="both", expand=True, padx=10, pady=5)
    
    # 시작 메시지
    result_text.insert(tk.END, "출발지와 도착지를 선택하고 '경로 검색' 버튼을 눌러주세요.\n")
    result_text.insert(tk.END, "원하는 우선순위를 선택하면 해당 경로만 표시됩니다.\n")
    
    # 상태 표시줄
    status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # 메인 루프 실행
    root.mainloop()