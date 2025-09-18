import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -------------------------
# --- Database Init -------
# -------------------------
def get_connection():
    conn = sqlite3.connect("tournament.db")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tournament (
        tournament_id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER,
        host_country TEXT,
        winner TEXT,
        runner_up TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Team (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name TEXT,
        coach_name TEXT,
        group_name TEXT,
        tournament_id INTEGER,
        FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Player (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        position TEXT,
        team_id INTEGER,
        FOREIGN KEY (team_id) REFERENCES Team(team_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Match (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        stage TEXT,
        team1_id INTEGER,
        team2_id INTEGER,
        team1_score INTEGER,
        team2_score INTEGER,
        tournament_id INTEGER,
        FOREIGN KEY (team1_id) REFERENCES Team(team_id),
        FOREIGN KEY (team2_id) REFERENCES Team(team_id),
        FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Event (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        player_id INTEGER,
        minute INTEGER,
        event_type TEXT,
        FOREIGN KEY (match_id) REFERENCES Match(match_id),
        FOREIGN KEY (player_id) REFERENCES Player(player_id)
    )
    """)
    conn.commit()
    conn.close()

# -------------------------
# --- Database CRUD -------
# -------------------------
# Tournament CRUD
def add_tournament(year, host_country, winner=None, runner_up=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tournament (year, host_country, winner, runner_up) VALUES (?, ?, ?, ?)",
                   (year, host_country, winner, runner_up))
    tid = cursor.lastrowid
    conn.commit()
    conn.close()
    return tid

def view_tournaments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tournament")
    data = cursor.fetchall()
    conn.close()
    return data

def edit_tournament(tid, year=None, host_country=None, winner=None, runner_up=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates, values = [], []
    if year is not None: updates.append("year=?"); values.append(year)
    if host_country: updates.append("host_country=?"); values.append(host_country)
    if winner: updates.append("winner=?"); values.append(winner)
    if runner_up: updates.append("runner_up=?"); values.append(runner_up)
    values.append(tid)
    cursor.execute(f"UPDATE Tournament SET {', '.join(updates)} WHERE tournament_id=?", values)
    conn.commit()
    conn.close()

def delete_tournament(tid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tournament WHERE tournament_id=?", (tid,))
    conn.commit()
    conn.close()

# Team CRUD
def add_team(team_name, coach_name, group_name, tournament_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Team (team_name, coach_name, group_name, tournament_id) VALUES (?, ?, ?, ?)",
                   (team_name, coach_name, group_name, tournament_id))
    tid = cursor.lastrowid
    conn.commit()
    conn.close()
    return tid

def view_teams(tournament_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if tournament_id:
        cursor.execute("SELECT * FROM Team WHERE tournament_id=?", (tournament_id,))
    else:
        cursor.execute("SELECT * FROM Team")
    data = cursor.fetchall()
    conn.close()
    return data

def edit_team(team_id, team_name=None, coach_name=None, group_name=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates, values = [], []
    if team_name: updates.append("team_name=?"); values.append(team_name)
    if coach_name: updates.append("coach_name=?"); values.append(coach_name)
    if group_name: updates.append("group_name=?"); values.append(group_name)
    values.append(team_id)
    cursor.execute(f"UPDATE Team SET {', '.join(updates)} WHERE team_id=?", values)
    conn.commit()
    conn.close()

def delete_team(team_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Team WHERE team_id=?", (team_id,))
    conn.commit()
    conn.close()

# Player CRUD
def add_player(player_name, position, team_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Player (player_name, position, team_id) VALUES (?, ?, ?)",
                   (player_name, position, team_id))
    pid = cursor.lastrowid
    conn.commit()
    conn.close()
    return pid

def view_players(team_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if team_id:
        cursor.execute("SELECT * FROM Player WHERE team_id=?", (team_id,))
    else:
        cursor.execute("SELECT * FROM Player")
    data = cursor.fetchall()
    conn.close()
    return data

def edit_player(player_id, player_name=None, position=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates, values = [], []
    if player_name: updates.append("player_name=?"); values.append(player_name)
    if position: updates.append("position=?"); values.append(position)
    values.append(player_id)
    cursor.execute(f"UPDATE Player SET {', '.join(updates)} WHERE player_id=?", values)
    conn.commit()
    conn.close()

def delete_player(player_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Player WHERE player_id=?", (player_id,))
    conn.commit()
    conn.close()

# Match CRUD
def add_match(date, stage, team1_id, team2_id, team1_score, team2_score, tournament_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Match (date, stage, team1_id, team2_id, team1_score, team2_score, tournament_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (date, stage, team1_id, team2_id, team1_score, team2_score, tournament_id))
    mid = cursor.lastrowid
    conn.commit()
    conn.close()
    return mid

def view_matches(tournament_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if tournament_id:
        cursor.execute("SELECT * FROM Match WHERE tournament_id=?", (tournament_id,))
    else:
        cursor.execute("SELECT * FROM Match")
    data = cursor.fetchall()
    conn.close()
    return data

def edit_match(match_id, date=None, stage=None, team1_score=None, team2_score=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates, values = [], []
    if date: updates.append("date=?"); values.append(date)
    if stage: updates.append("stage=?"); values.append(stage)
    if team1_score is not None: updates.append("team1_score=?"); values.append(team1_score)
    if team2_score is not None: updates.append("team2_score=?"); values.append(team2_score)
    values.append(match_id)
    cursor.execute(f"UPDATE Match SET {', '.join(updates)} WHERE match_id=?", values)
    conn.commit()
    conn.close()

def delete_match(match_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Match WHERE match_id=?", (match_id,))
    conn.commit()
    conn.close()

# Event CRUD
def add_event(match_id, player_id, minute, event_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Event (match_id, player_id, minute, event_type) VALUES (?, ?, ?, ?)",
                   (match_id, player_id, minute, event_type))
    eid = cursor.lastrowid
    conn.commit()
    conn.close()
    return eid

def view_events(match_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if match_id:
        cursor.execute("SELECT * FROM Event WHERE match_id=?", (match_id,))
    else:
        cursor.execute("SELECT * FROM Event")
    data = cursor.fetchall()
    conn.close()
    return data

def edit_event(event_id, minute=None, event_type=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates, values = [], []
    if minute is not None: updates.append("minute=?"); values.append(minute)
    if event_type: updates.append("event_type=?"); values.append(event_type)
    values.append(event_id)
    cursor.execute(f"UPDATE Event SET {', '.join(updates)} WHERE event_id=?", values)
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Event WHERE event_id=?", (event_id,))
    conn.commit()
    conn.close()



# -----------------------------
# --- Analysis / Visualize ----
# -----------------------------

# Leaderboard per Tournament (Bar chart)
def leaderboard_form():
    def generate():
        tid = tid_entry.get()
        if not tid:
            messagebox.showerror("Error", "Tournament ID required")
            return
        tid = int(tid)

        conn = sqlite3.connect("tournament.db")
        df_matches = pd.read_sql_query(f"SELECT * FROM Match WHERE tournament_id={tid}", conn)
        df_teams = pd.read_sql_query(f"SELECT * FROM Team WHERE tournament_id={tid}", conn)
        conn.close()

        points = {team_id:0 for team_id in df_teams['team_id']}
        goals_for = {team_id:0 for team_id in df_teams['team_id']}
        goals_against = {team_id:0 for team_id in df_teams['team_id']}

        for _, row in df_matches.iterrows():
            t1, t2 = row['team1_id'], row['team2_id']
            s1, s2 = row['team1_score'], row['team2_score']
            goals_for[t1] += s1; goals_for[t2] += s2
            goals_against[t1] += s2; goals_against[t2] += s1
            if s1 > s2: points[t1] += 3
            elif s1 < s2: points[t2] += 3
            else: points[t1] += 1; points[t2] += 1

        table_win = tk.Toplevel(root)
        table_win.title("Leaderboard")
        tree = ttk.Treeview(table_win, columns=("Team", "Points", "GF", "GA"), show="headings")
        for col in ["Team", "Points", "GF", "GA"]: tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        names, pts = [], []
        for tid_team, team_name in zip(df_teams['team_id'], df_teams['team_name']):
            tree.insert("", "end", values=(team_name, points[tid_team], goals_for[tid_team], goals_against[tid_team]))
            names.append(team_name)
            pts.append(points[tid_team])

        # Bar chart
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(names, pts, color='skyblue')
        ax.set_ylabel("Points")
        ax.set_title("Leaderboard")
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        canvas = FigureCanvasTkAgg(fig, master=table_win)
        canvas.draw()
        canvas.get_tk_widget().pack()

    form = tk.Toplevel(root)
    form.title("Leaderboard")
    tk.Label(form, text="Tournament ID:").pack(pady=5)
    tid_entry = tk.Entry(form)
    tid_entry.pack(pady=5)
    tk.Button(form, text="Generate Leaderboard", command=generate).pack(pady=10)


# Top Players per Tournament (Pie chart)
def top_players_form():
    def generate():
        tid = tid_entry.get()
        if not tid:
            messagebox.showerror("Error", "Tournament ID required")
            return
        tid = int(tid)

        conn = sqlite3.connect("tournament.db")
        df_matches = pd.read_sql_query(f"SELECT match_id FROM Match WHERE tournament_id={tid}", conn)
        match_ids = df_matches['match_id'].tolist()
        if not match_ids:
            messagebox.showinfo("Info", "No matches found")
            conn.close()
            return
        match_ids_str = ",".join(map(str, match_ids))
        df_events = pd.read_sql_query(f"SELECT * FROM Event WHERE match_id IN ({match_ids_str}) AND event_type='Goal'", conn)
        df_players = pd.read_sql_query("SELECT * FROM Player", conn)
        conn.close()

        goal_counts = df_events['player_id'].value_counts().to_dict()

        table_win = tk.Toplevel(root)
        table_win.title("Top Players")
        tree = ttk.Treeview(table_win, columns=("Player", "Goals"), show="headings")
        tree.heading("Player", text="Player")
        tree.heading("Goals", text="Goals")
        tree.pack(fill=tk.BOTH, expand=True)

        labels, goals = [], []
        for pid, count in goal_counts.items():
            name = df_players[df_players['player_id']==pid]['player_name'].values[0]
            tree.insert("", "end", values=(name, count))
            labels.append(name)
            goals.append(count)

        # Pie chart
        fig, ax = plt.subplots(figsize=(6,6))
        ax.pie(goals, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.set_title("Top Goal Scorers")
        canvas = FigureCanvasTkAgg(fig, master=table_win)
        canvas.draw()
        canvas.get_tk_widget().pack()

    form = tk.Toplevel(root)
    form.title("Top Players")
    tk.Label(form, text="Tournament ID:").pack(pady=5)
    tid_entry = tk.Entry(form)
    tid_entry.pack(pady=5)
    tk.Button(form, text="Show Top Players", command=generate).pack(pady=10)


# Match Key Events by Match ID (Scatter plot)
def match_events_form():
    def generate():
        mid = mid_entry.get()
        if not mid:
            messagebox.showerror("Error", "Match ID required")
            return
        mid = int(mid)

        conn = sqlite3.connect("tournament.db")
        df_events = pd.read_sql_query(f"SELECT * FROM Event WHERE match_id={mid}", conn)
        df_players = pd.read_sql_query("SELECT * FROM Player", conn)
        conn.close()

        df_events['player_name'] = df_events['player_id'].apply(lambda x: df_players[df_players['player_id']==x]['player_name'].values[0])

        table_win = tk.Toplevel(root)
        table_win.title("Match Key Events")
        tree = ttk.Treeview(table_win, columns=("Minute", "Player", "Event"), show="headings")
        for col in ["Minute", "Player", "Event"]: tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        for _, row in df_events.iterrows():
            tree.insert("", "end", values=(row['minute'], row['player_name'], row['event_type']))

        # Scatter plot
        fig, ax = plt.subplots(figsize=(8,4))
        colors = {'Goal':'green','Save':'red','Assist':'blue','Shot on target':'orange'}
        for _, row in df_events.iterrows():
            ax.scatter(row['player_name'], row['minute'], color=colors.get(row['event_type'],'black'), s=100, label=row['event_type'])
        ax.set_ylabel("Minute")
        ax.set_xlabel("Player")
        ax.set_title("Match Key Events")
        ax.legend(colors.keys())
        ax.set_xticks(range(len(df_events['player_name'])))
        ax.set_xticklabels(df_events['player_name'], rotation=45, ha='right')
        canvas = FigureCanvasTkAgg(fig, master=table_win)
        canvas.draw()
        canvas.get_tk_widget().pack()

    form = tk.Toplevel(root)
    form.title("Match Key Events")
    tk.Label(form, text="Match ID:").pack(pady=5)
    mid_entry = tk.Entry(form)
    mid_entry.pack(pady=5)
    tk.Button(form, text="Show Match Events", command=generate).pack(pady=10)


# Tournament Trends (Total Goals per Team)
def tournament_trends_form():
    def generate():
        tid = tid_entry.get()
        if not tid:
            messagebox.showerror("Error", "Tournament ID required")
            return
        tid = int(tid)

        conn = sqlite3.connect("tournament.db")
        df_matches = pd.read_sql_query(f"SELECT * FROM Match WHERE tournament_id={tid}", conn)
        df_teams = pd.read_sql_query(f"SELECT * FROM Team WHERE tournament_id={tid}", conn)
        conn.close()

        goals_per_team = {team_id:0 for team_id in df_teams['team_id']}
        for _, row in df_matches.iterrows():
            goals_per_team[row['team1_id']] += row['team1_score']
            goals_per_team[row['team2_id']] += row['team2_score']

        table_win = tk.Toplevel(root)
        table_win.title("Tournament Trends")
        tree = ttk.Treeview(table_win, columns=("Team", "Goals"), show="headings")
        tree.heading("Team", text="Team")
        tree.heading("Goals", text="Goals")
        tree.pack(fill=tk.BOTH, expand=True)

        names, goals = [], []
        for tid_team, team_name in zip(df_teams['team_id'], df_teams['team_name']):
            tree.insert("", "end", values=(team_name, goals_per_team[tid_team]))
            names.append(team_name)
            goals.append(goals_per_team[tid_team])

        # Bar chart
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(names, goals, color='purple')
        ax.set_ylabel("Goals")
        ax.set_title("Goals per Team in Tournament")
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        canvas = FigureCanvasTkAgg(fig, master=table_win)
        canvas.draw()
        canvas.get_tk_widget().pack()

    form = tk.Toplevel(root)
    form.title("Tournament Trends")
    tk.Label(form, text="Tournament ID:").pack(pady=5)
    tid_entry = tk.Entry(form)
    tid_entry.pack(pady=5)
    tk.Button(form, text="Generate Tournament Trends", command=generate).pack(pady=10)

# -------------------------
# --- Tkinter GUI ----------
# -------------------------
root = tk.Tk()
root.title("Tournament Analyser")
root.geometry("1000x600")

# GUI helpers and menu will be same as described in my previous message

# --- Add Team Form ---
def add_team_form():
    def submit():
        name = name_entry.get()
        coach = coach_entry.get()
        group = group_entry.get()
        tournament_id = tid_entry.get()
        if not name or not coach or not group or not tournament_id:
            messagebox.showerror("Error", "All fields required")
            return
        try:
            tid = int(tournament_id)
        except:
            messagebox.showerror("Error", "Tournament ID must be a number")
            return
        team_id = add_team(name, coach, group, tid)
        messagebox.showinfo("Success", f"Team added with ID {team_id}")
        form.destroy()

    form = tk.Toplevel(root)
    form.title("Add Team")
    
    tk.Label(form, text="Team Name:").grid(row=0, column=0, pady=5, padx=5)
    tk.Label(form, text="Coach Name:").grid(row=1, column=0, pady=5, padx=5)
    tk.Label(form, text="Group Name:").grid(row=2, column=0, pady=5, padx=5)
    tk.Label(form, text="Tournament ID:").grid(row=3, column=0, pady=5, padx=5)
    
    name_entry = tk.Entry(form)
    coach_entry = tk.Entry(form)
    group_entry = tk.Entry(form)
    tid_entry = tk.Entry(form)
    
    name_entry.grid(row=0, column=1, pady=5, padx=5)
    coach_entry.grid(row=1, column=1, pady=5, padx=5)
    group_entry.grid(row=2, column=1, pady=5, padx=5)
    tid_entry.grid(row=3, column=1, pady=5, padx=5)
    
    tk.Button(form, text="Add", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

# --- View/Edit/Delete Teams Table ---
def view_teams_table():
    # Ask for Tournament ID first
    tournament_id = simpledialog.askinteger("Input", "Enter Tournament ID:")
    if tournament_id is None:
        return

    table_win = tk.Toplevel(root)
    table_win.title(f"Teams in Tournament {tournament_id}")

    tree = ttk.Treeview(table_win, columns=("ID", "Name", "Coach", "Group", "TournamentID"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Team Name")
    tree.heading("Coach", text="Coach")
    tree.heading("Group", text="Group")
    tree.heading("TournamentID", text="Tournament ID")
    tree.pack(fill=tk.BOTH, expand=True)

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        data = view_teams(tournament_id)
        for t in data:
            tree.insert("", "end", values=t)

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a team to edit")
            return
        tid = tree.item(selected[0])['values'][0]
        name = simpledialog.askstring("Edit", "Team Name:", initialvalue=tree.item(selected[0])['values'][1])
        coach = simpledialog.askstring("Edit", "Coach Name:", initialvalue=tree.item(selected[0])['values'][2])
        group = simpledialog.askstring("Edit", "Group:", initialvalue=tree.item(selected[0])['values'][3])
        edit_team(tid, name, coach, group)
        refresh()

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a team to delete")
            return
        tid = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this team?"):
            delete_team(tid)
            refresh()

    btn_frame = tk.Frame(table_win)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text="Edit Selected", command=edit_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Refresh", command=refresh).pack(side=tk.LEFT, padx=5, pady=5)

    refresh()

# --- Add Match Form ---
def add_match_form():
    form = tk.Toplevel(root)
    form.title("Add Match")

    tk.Label(form, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(form, text="Stage:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(form, text="Team 1 ID:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(form, text="Team 2 ID:").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(form, text="Team 1 Score:").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(form, text="Team 2 Score:").grid(row=5, column=0, padx=5, pady=5)
    tk.Label(form, text="Tournament ID:").grid(row=6, column=0, padx=5, pady=5)

    date_entry = tk.Entry(form)
    stage_entry = tk.Entry(form)
    team1_entry = tk.Entry(form)
    team2_entry = tk.Entry(form)
    score1_entry = tk.Entry(form)
    score2_entry = tk.Entry(form)
    tournament_entry = tk.Entry(form)

    date_entry.grid(row=0, column=1, padx=5, pady=5)
    stage_entry.grid(row=1, column=1, padx=5, pady=5)
    team1_entry.grid(row=2, column=1, padx=5, pady=5)
    team2_entry.grid(row=3, column=1, padx=5, pady=5)
    score1_entry.grid(row=4, column=1, padx=5, pady=5)
    score2_entry.grid(row=5, column=1, padx=5, pady=5)
    tournament_entry.grid(row=6, column=1, padx=5, pady=5)

    def submit():
        try:
            date = date_entry.get()
            stage = stage_entry.get()
            team1 = int(team1_entry.get())
            team2 = int(team2_entry.get())
            score1 = int(score1_entry.get())
            score2 = int(score2_entry.get())
            tid = int(tournament_entry.get())

            mid = add_match(date, stage, team1, team2, score1, score2, tid)
            messagebox.showinfo("Success", f"Match added with ID {mid}")
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add match:\n{e}")

    tk.Button(form, text="Add Match", command=submit).grid(row=7, column=0, columnspan=2, pady=10)


# --- View/Edit/Delete Matches Table ---
def view_matches_table():
    # Ask for Tournament ID first
    tournament_id = simpledialog.askinteger("Input", "Enter Tournament ID:")
    if tournament_id is None:
        return

    table_win = tk.Toplevel(root)
    table_win.title(f"Matches for Tournament {tournament_id}")

    tree = ttk.Treeview(table_win, columns=("ID","Date","Stage","Team1","Team2","Score1","Score2","TournamentID"), show="headings")
    tree.heading("ID", text="Match ID")
    tree.heading("Date", text="Date")
    tree.heading("Stage", text="Stage")
    tree.heading("Team1", text="Team 1 ID")
    tree.heading("Team2", text="Team 2 ID")
    tree.heading("Score1", text="Team 1 Score")
    tree.heading("Score2", text="Team 2 Score")
    tree.heading("TournamentID", text="Tournament ID")
    tree.pack(fill=tk.BOTH, expand=True)

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        data = view_matches(tournament_id)
        for m in data:
            tree.insert("", "end", values=m)

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a match to edit")
            return
        mid = tree.item(selected[0])['values'][0]
        date = simpledialog.askstring("Edit", "Date:", initialvalue=tree.item(selected[0])['values'][1])
        stage = simpledialog.askstring("Edit", "Stage:", initialvalue=tree.item(selected[0])['values'][2])
        score1 = simpledialog.askinteger("Edit", "Team 1 Score:", initialvalue=tree.item(selected[0])['values'][5])
        score2 = simpledialog.askinteger("Edit", "Team 2 Score:", initialvalue=tree.item(selected[0])['values'][6])
        edit_match(mid, date, stage, score1, score2)
        refresh()

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a match to delete")
            return
        mid = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this match?"):
            delete_match(mid)
            refresh()

    btn_frame = tk.Frame(table_win)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text="Edit Selected", command=edit_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Refresh", command=refresh).pack(side=tk.LEFT, padx=5, pady=5)

    refresh()


# Add Tournament Form
def add_tournament_form():
    def submit():
        year = year_entry.get()
        host = host_entry.get()
        winner = winner_entry.get()
        runner_up = runner_entry.get()
        if not year or not host:
            messagebox.showerror("Error", "Year and Host Country required")
            return
        tid = add_tournament(int(year), host, winner, runner_up)
        messagebox.showinfo("Success", f"Tournament added with ID {tid}")
        form.destroy()

    form = tk.Toplevel(root)
    form.title("Add Tournament")
    tk.Label(form, text="Year:").grid(row=0, column=0, pady=5, padx=5)
    tk.Label(form, text="Host Country:").grid(row=1, column=0, pady=5, padx=5)
    tk.Label(form, text="Winner:").grid(row=2, column=0, pady=5, padx=5)
    tk.Label(form, text="Runner-up:").grid(row=3, column=0, pady=5, padx=5)

    year_entry = tk.Entry(form)
    host_entry = tk.Entry(form)
    winner_entry = tk.Entry(form)
    runner_entry = tk.Entry(form)

    year_entry.grid(row=0, column=1, pady=5, padx=5)
    host_entry.grid(row=1, column=1, pady=5, padx=5)
    winner_entry.grid(row=2, column=1, pady=5, padx=5)
    runner_entry.grid(row=3, column=1, pady=5, padx=5)

    tk.Button(form, text="Add", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

# View/Edit/Delete Tournaments
def view_tournaments_table():
    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        data = view_tournaments()
        for t in data:
            tree.insert("", "end", values=t)

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a tournament to edit")
            return
        tid = tree.item(selected[0])['values'][0]
        year = simpledialog.askinteger("Edit", "Year:", initialvalue=tree.item(selected[0])['values'][1])
        host = simpledialog.askstring("Edit", "Host Country:", initialvalue=tree.item(selected[0])['values'][2])
        winner = simpledialog.askstring("Edit", "Winner:", initialvalue=tree.item(selected[0])['values'][3])
        runner_up = simpledialog.askstring("Edit", "Runner-up:", initialvalue=tree.item(selected[0])['values'][4])
        edit_tournament(tid, year, host, winner, runner_up)
        refresh()

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a tournament to delete")
            return
        tid = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this tournament?"):
            delete_tournament(tid)
            refresh()

    table_win = tk.Toplevel(root)
    table_win.title("View Tournaments")
    tree = ttk.Treeview(table_win, columns=("ID", "Year", "Host", "Winner", "RunnerUp"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Year", text="Year")
    tree.heading("Host", text="Host Country")
    tree.heading("Winner", text="Winner")
    tree.heading("RunnerUp", text="Runner-up")
    tree.pack(fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(table_win)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text="Edit Selected", command=edit_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Refresh", command=refresh).pack(side=tk.LEFT, padx=5, pady=5)

    refresh()

# -----------------------------
# --- Add Player Form ----------
# -----------------------------
def add_player_form():
    team_id = simpledialog.askinteger("Team ID", "Enter Team ID for the player:")
    if team_id is None:
        return

    def submit():
        name = name_entry.get()
        position = pos_entry.get()
        if not name or not position:
            messagebox.showerror("Error", "Name and Position required")
            return
        pid = add_player(name, position, team_id)
        messagebox.showinfo("Success", f"Player added with ID {pid}")
        form.destroy()

    form = tk.Toplevel(root)
    form.title("Add Player")
    tk.Label(form, text="Player Name:").grid(row=0, column=0, pady=5, padx=5)
    tk.Label(form, text="Position:").grid(row=1, column=0, pady=5, padx=5)
    name_entry = tk.Entry(form)
    pos_entry = tk.Entry(form)
    name_entry.grid(row=0, column=1, pady=5, padx=5)
    pos_entry.grid(row=1, column=1, pady=5, padx=5)
    tk.Button(form, text="Add Player", command=submit).grid(row=2, column=0, columnspan=2, pady=10)


# -----------------------------
# --- View/Edit/Delete Players -
# -----------------------------
def view_players_table():
    team_id = simpledialog.askinteger("Team ID", "Enter Team ID to view players:")
    if team_id is None:
        return

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        data = view_players(team_id)
        for p in data:
            tree.insert("", "end", values=p)

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a player to edit")
            return
        pid = tree.item(selected[0])['values'][0]
        name = simpledialog.askstring("Edit", "Player Name:", initialvalue=tree.item(selected[0])['values'][1])
        position = simpledialog.askstring("Edit", "Position:", initialvalue=tree.item(selected[0])['values'][2])
        edit_player(pid, name, position)
        refresh()

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a player to delete")
            return
        pid = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this player?"):
            delete_player(pid)
            refresh()

    table_win = tk.Toplevel(root)
    table_win.title(f"Players of Team {team_id}")
    tree = ttk.Treeview(table_win, columns=("ID", "Name", "Position", "Team ID"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Position", text="Position")
    tree.heading("Team ID", text="Team ID")
    tree.pack(fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(table_win)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text="Edit Selected", command=edit_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Refresh", command=refresh).pack(side=tk.LEFT, padx=5, pady=5)

    refresh()


# -----------------------------
# --- Add Event Form ----------
# -----------------------------
def add_event_form():
    match_id = simpledialog.askinteger("Match ID", "Enter Match ID for the event:")
    if match_id is None:
        return

    player_id = simpledialog.askinteger("Player ID", "Enter Player ID for this event:")
    if player_id is None:
        return

    def submit():
        minute = minute_entry.get()
        event_type = event_entry.get()
        if not minute or not event_type:
            messagebox.showerror("Error", "Minute and Event Type required")
            return
        eid = add_event(match_id, player_id, int(minute), event_type)
        messagebox.showinfo("Success", f"Event added with ID {eid}")
        form.destroy()

    form = tk.Toplevel(root)
    form.title("Add Event")
    tk.Label(form, text="Minute:").grid(row=0, column=0, pady=5, padx=5)
    tk.Label(form, text="Event Type:").grid(row=1, column=0, pady=5, padx=5)
    minute_entry = tk.Entry(form)
    event_entry = tk.Entry(form)
    minute_entry.grid(row=0, column=1, pady=5, padx=5)
    event_entry.grid(row=1, column=1, pady=5, padx=5)
    tk.Button(form, text="Add Event", command=submit).grid(row=2, column=0, columnspan=2, pady=10)


# -----------------------------
# --- View/Edit/Delete Events -
# -----------------------------
def view_events_table():
    match_id = simpledialog.askinteger("Match ID", "Enter Match ID to view events:")
    if match_id is None:
        return

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        data = view_events(match_id)
        for e in data:
            tree.insert("", "end", values=e)

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an event to edit")
            return
        eid = tree.item(selected[0])['values'][0]
        minute = simpledialog.askinteger("Edit", "Minute:", initialvalue=tree.item(selected[0])['values'][3])
        event_type = simpledialog.askstring("Edit", "Event Type:", initialvalue=tree.item(selected[0])['values'][4])
        edit_event(eid, minute, event_type)
        refresh()

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an event to delete")
            return
        eid = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this event?"):
            delete_event(eid)
            refresh()

    table_win = tk.Toplevel(root)
    table_win.title(f"Events of Match {match_id}")
    tree = ttk.Treeview(table_win, columns=("ID", "Match ID", "Player ID", "Minute", "Event Type"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Match ID", text="Match ID")
    tree.heading("Player ID", text="Player ID")
    tree.heading("Minute", text="Minute")
    tree.heading("Event Type", text="Event Type")
    tree.pack(fill=tk.BOTH, expand=True)

    btn_frame = tk.Frame(table_win)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text="Edit Selected", command=edit_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Refresh", command=refresh).pack(side=tk.LEFT, padx=5, pady=5)

    refresh()



if __name__ == "__main__":
    if os.path.exists("tournament.db"):
        os.remove("tournament.db")

    init_db()

    ##DATA SET
    # -----------------------------
    # --- Tournaments -------------
    # -----------------------------
    tid2010 = add_tournament(2010, "South Africa", "Spain", "Netherlands")
    tid2014 = add_tournament(2014, "Brazil", "Germany", "Argentina")
    tid2018 = add_tournament(2018, "Russia", "France", "Croatia")
    tid2022 = add_tournament(2022, "Qatar", "Argentina", "France")

    # -----------------------------
    # --- Teams -------------------
    # -----------------------------
    # 2010
    t2010_spain = add_team("Spain", "Vicente del Bosque", "H", tid2010)
    t2010_netherlands = add_team("Netherlands", "Bert van Marwijk", "E", tid2010)
    t2010_germany = add_team("Germany", "Joachim Löw", "D", tid2010)
    t2010_uruguay = add_team("Uruguay", "Óscar Tabárez", "A", tid2010)
    t2010_ghana = add_team("Ghana", "Milovan Rajevac", "D", tid2010)
    t2010_brazil = add_team("Brazil", "Dunga", "G", tid2010)
    t2010_argentina = add_team("Argentina", "Diego Maradona", "B", tid2010)
    t2010_england = add_team("England", "Fabio Capello", "C", tid2010)
    t2010_france = add_team("France", "Raymond Domenech", "A", tid2010)
    t2010_italy = add_team("Italy", "Marcello Lippi", "F", tid2010)

    # 2014
    t2014_germany = add_team("Germany", "Joachim Löw", "G", tid2014)
    t2014_argentina = add_team("Argentina", "Alejandro Sabella", "F", tid2014)
    t2014_brazil = add_team("Brazil", "Luiz Felipe Scolari", "A", tid2014)
    t2014_netherlands = add_team("Netherlands", "Louis van Gaal", "B", tid2014)
    t2014_belgium = add_team("Belgium", "Marc Wilmots", "H", tid2014)
    t2014_france = add_team("France", "Didier Deschamps", "E", tid2014)
    t2014_chile = add_team("Chile", "Jorge Sampaoli", "D", tid2014)
    t2014_colombia = add_team("Colombia", "José Pekerman", "C", tid2014)
    t2014_mexico = add_team("Mexico", "Miguel Herrera", "A", tid2014)
    t2014_uruguay = add_team("Uruguay", "Óscar Tabárez", "B", tid2014)

    # 2018
    t2018_france = add_team("France", "Didier Deschamps", "C", tid2018)
    t2018_croatia = add_team("Croatia", "Zlatko Dalić", "D", tid2018)
    t2018_belgium = add_team("Belgium", "Roberto Martínez", "G", tid2018)
    t2018_england = add_team("England", "Gareth Southgate", "G", tid2018)
    t2018_brazil = add_team("Brazil", "Tite", "E", tid2018)
    t2018_russia = add_team("Russia", "Stanislav Cherchesov", "A", tid2018)
    t2018_sweden = add_team("Sweden", "Jan Andersson", "F", tid2018)
    t2018_uruguay = add_team("Uruguay", "Óscar Tabárez", "A", tid2018)
    t2018_portugal = add_team("Portugal", "Fernando Santos", "B", tid2018)
    t2018_spain = add_team("Spain", "Fernando Hierro", "B", tid2018)

    # 2022
    t2022_argentina = add_team("Argentina", "Lionel Scaloni", "C", tid2022)
    t2022_france = add_team("France", "Didier Deschamps", "D", tid2022)
    t2022_croatia = add_team("Croatia", "Zlatko Dalić", "F", tid2022)
    t2022_morocco = add_team("Morocco", "Walid Regragui", "F", tid2022)
    t2022_brazil = add_team("Brazil", "Tite", "G", tid2022)
    t2022_england = add_team("England", "Gareth Southgate", "B", tid2022)
    t2022_portugal = add_team("Portugal", "Fernando Santos", "H", tid2022)
    t2022_netherlands = add_team("Netherlands", "Louis van Gaal", "A", tid2022)
    t2022_germany = add_team("Germany", "Hansi Flick", "E", tid2022)
    t2022_spain = add_team("Spain", "Luis Enrique", "D", tid2022)


    # -----------------------------
    # --- Players -----------------
    # -----------------------------
    p2010_players = [
        add_player("Andres Iniesta", "Midfielder", t2010_spain),
        add_player("Iker Casillas", "Goalkeeper", t2010_spain),
        add_player("Xavi", "Midfielder", t2010_spain),
        add_player("David Villa", "Forward", t2010_spain),
        add_player("Wesley Sneijder", "Midfielder", t2010_netherlands),
        add_player("Robin van Persie", "Forward", t2010_netherlands),
        add_player("Rafael van der Vaart", "Midfielder", t2010_netherlands),
        add_player("Arjen Robben", "Forward", t2010_netherlands),
        add_player("Miroslav Klose", "Forward", t2010_germany),
        add_player("Thomas Müller", "Forward", t2010_germany),
        add_player("Lukas Podolski", "Forward", t2010_germany),
        add_player("Diego Forlán", "Forward", t2010_uruguay),
        add_player("Luis Suárez", "Forward", t2010_uruguay),
        add_player("Edinson Cavani", "Forward", t2010_uruguay),
        add_player("Asamoah Gyan", "Forward", t2010_ghana),
        add_player("Kevin-Prince Boateng", "Midfielder", t2010_ghana),
        add_player("Kaka", "Midfielder", t2010_brazil),
        add_player("Neymar", "Forward", t2010_brazil),
        add_player("Lionel Messi", "Forward", t2010_argentina),
        add_player("Sergio Agüero", "Forward", t2010_argentina),
        add_player("Wayne Rooney", "Forward", t2010_england),
        add_player("Frank Lampard", "Midfielder", t2010_england),
        add_player("Franck Ribéry", "Midfielder", t2010_france),
        add_player("Karim Benzema", "Forward", t2010_france),
        add_player("Gianluigi Buffon", "Goalkeeper", t2010_italy),
        add_player("Andrea Pirlo", "Midfielder", t2010_italy),
        add_player("Daniele De Rossi", "Midfielder", t2010_italy),
        add_player("Thiago Silva", "Defender", t2010_brazil),
        add_player("Xabi Alonso", "Midfielder", t2010_spain),
        add_player("David Beckham", "Midfielder", t2010_england)
    ]




    # 2014 Germany & Argentina & others
    p2014_players = [
        # Germany
        add_player("Mario Götze", "Forward", t2014_germany),
        add_player("Manuel Neuer", "Goalkeeper", t2014_germany),
        add_player("Toni Kroos", "Midfielder", t2014_germany),
        add_player("Philipp Lahm", "Defender", t2014_germany),
        add_player("Thomas Müller", "Forward", t2014_germany),
        add_player("Mats Hummels", "Defender", t2014_germany),
        add_player("Bastian Schweinsteiger", "Midfielder", t2014_germany),
        # Argentina
        add_player("Lionel Messi", "Forward", t2014_argentina),
        add_player("Sergio Agüero", "Forward", t2014_argentina),
        add_player("Gonzalo Higuaín", "Forward", t2014_argentina),
        add_player("Ezequiel Lavezzi", "Midfielder", t2014_argentina),
        add_player("Javier Mascherano", "Midfielder", t2014_argentina),
        add_player("Sergio Romero", "Goalkeeper", t2014_argentina),
        # Brazil
        add_player("Neymar", "Forward", t2014_brazil),
        add_player("Hulk", "Forward", t2014_brazil),
        add_player("Oscar", "Midfielder", t2014_brazil),
        add_player("Thiago Silva", "Defender", t2014_brazil),
        add_player("David Luiz", "Defender", t2014_brazil),
        add_player("Julio Cesar", "Goalkeeper", t2014_brazil),
        # Netherlands
        add_player("Robin van Persie", "Forward", t2014_netherlands),
        add_player("Wesley Sneijder", "Midfielder", t2014_netherlands),
        add_player("Arjen Robben", "Forward", t2014_netherlands),
        add_player("Daryl Janmaat", "Defender", t2014_netherlands),
        add_player("Maarten Stekelenburg", "Goalkeeper", t2014_netherlands),
        # Belgium
        add_player("Eden Hazard", "Forward", t2014_belgium),
        add_player("Kevin De Bruyne", "Midfielder", t2014_belgium),
        add_player("Vincent Kompany", "Defender", t2014_belgium),
        # France
        add_player("Antoine Griezmann", "Forward", t2014_france),
        add_player("Paul Pogba", "Midfielder", t2014_france),
        add_player("Hugo Lloris", "Goalkeeper", t2014_france)
    ]

    # 2018 France & Croatia & others
    p2018_players = [
        # France
        add_player("Kylian Mbappé", "Forward", t2018_france),
        add_player("Antoine Griezmann", "Forward", t2018_france),
        add_player("Paul Pogba", "Midfielder", t2018_france),
        add_player("N'Golo Kanté", "Midfielder", t2018_france),
        add_player("Hugo Lloris", "Goalkeeper", t2018_france),
        add_player("Raphaël Varane", "Defender", t2018_france),
        add_player("Samuel Umtiti", "Defender", t2018_france),
        # Croatia
        add_player("Luka Modric", "Midfielder", t2018_croatia),
        add_player("Ivan Rakitic", "Midfielder", t2018_croatia),
        add_player("Mario Mandzukic", "Forward", t2018_croatia),
        add_player("Danijel Subasic", "Goalkeeper", t2018_croatia),
        add_player("Dejan Lovren", "Defender", t2018_croatia),
        add_player("Domagoj Vida", "Defender", t2018_croatia),
        # Belgium
        add_player("Eden Hazard", "Forward", t2018_belgium),
        add_player("Romelu Lukaku", "Forward", t2018_belgium),
        add_player("Kevin De Bruyne", "Midfielder", t2018_belgium),
        add_player("Thibaut Courtois", "Goalkeeper", t2018_belgium),
        add_player("Jan Vertonghen", "Defender", t2018_belgium),
        # England
        add_player("Harry Kane", "Forward", t2018_england),
        add_player("Raheem Sterling", "Forward", t2018_england),
        add_player("Jordan Henderson", "Midfielder", t2018_england),
        add_player("Jordan Pickford", "Goalkeeper", t2018_england),
        add_player("Harry Maguire", "Defender", t2018_england),
        # Brazil
        add_player("Neymar", "Forward", t2018_brazil),
        add_player("Philippe Coutinho", "Midfielder", t2018_brazil),
        add_player("Marcelo", "Defender", t2018_brazil),
        add_player("Alisson Becker", "Goalkeeper", t2018_brazil),
        # Russia
        add_player("Artem Dzyuba", "Forward", t2018_russia),
        add_player("Igor Akinfeev", "Goalkeeper", t2018_russia),
        add_player("Denis Cheryshev", "Midfielder", t2018_russia)
    ]

    # 2022 Argentina & France & others
    p2022_players = [
        # Argentina
        add_player("Lionel Messi", "Forward", t2022_argentina),
        add_player("Paulo Dybala", "Forward", t2022_argentina),
        add_player("Enzo Fernández", "Midfielder", t2022_argentina),
        add_player("Emiliano Martínez", "Goalkeeper", t2022_argentina),
        add_player("Rodrigo De Paul", "Midfielder", t2022_argentina),
        add_player("Lautaro Martínez", "Forward", t2022_argentina),
        add_player("Nicolás Otamendi", "Defender", t2022_argentina),
        # France
        add_player("Kylian Mbappé", "Forward", t2022_france),
        add_player("Antoine Griezmann", "Forward", t2022_france),
        add_player("Paul Pogba", "Midfielder", t2022_france),
        add_player("Hugo Lloris", "Goalkeeper", t2022_france),
        add_player("Raphaël Varane", "Defender", t2022_france),
        add_player("Olivier Giroud", "Forward", t2022_france),
        # Croatia
        add_player("Luka Modric", "Midfielder", t2022_croatia),
        add_player("Ivan Perišić", "Forward", t2022_croatia),
        add_player("Domagoj Vida", "Defender", t2022_croatia),
        add_player("Lovre Kalinić", "Goalkeeper", t2022_croatia),
        # Morocco
        add_player("Achraf Hakimi", "Defender", t2022_morocco),
        add_player("Youssef En-Nesyri", "Forward", t2022_morocco),
        add_player("Sofyan Amrabat", "Midfielder", t2022_morocco),
        add_player("Yassine Bounou", "Goalkeeper", t2022_morocco),
        # Brazil
        add_player("Neymar", "Forward", t2022_brazil),
        add_player("Vinicius Jr.", "Forward", t2022_brazil),
        add_player("Casemiro", "Midfielder", t2022_brazil),
        # England
        add_player("Harry Kane", "Forward", t2022_england),
        add_player("Phil Foden", "Midfielder", t2022_england),
        add_player("Jordan Pickford", "Goalkeeper", t2022_england),
        # Portugal
        add_player("Cristiano Ronaldo", "Forward", t2022_portugal),
        add_player("Bruno Fernandes", "Midfielder", t2022_portugal),
        add_player("Rui Patricio", "Goalkeeper", t2022_portugal)
    ]

    # -----------------------------
    # --- Matches -----------------
    # -----------------------------
    m2010_matches = [
        add_match("2010-06-11", "Group", t2010_spain, t2010_netherlands, 1, 0, tid2010),
        add_match("2010-06-12", "Group", t2010_uruguay, t2010_germany, 0, 0, tid2010),
        add_match("2010-06-13", "Group", t2010_ghana, t2010_brazil, 1, 2, tid2010),
        add_match("2010-06-14", "Group", t2010_argentina, t2010_england, 2, 1, tid2010),
        add_match("2010-06-15", "Group", t2010_france, t2010_italy, 0, 0, tid2010),
        add_match("2010-06-20", "Round of 16", t2010_spain, t2010_ghana, 1, 0, tid2010),
        add_match("2010-06-21", "Round of 16", t2010_germany, t2010_uruguay, 4, 2, tid2010),
        add_match("2010-06-25", "Quarterfinal", t2010_spain, t2010_germany, 1, 0, tid2010),
        add_match("2010-07-07", "Semifinal", t2010_netherlands, t2010_uruguay, 3, 2, tid2010),
        add_match("2010-07-11", "Final", t2010_spain, t2010_netherlands, 1, 0, tid2010)
    ]

    # 2014 Germany tournament matches
    m2014_1 = add_match("2014-06-12", "Group", t2014_brazil, t2014_mexico, 3, 1, tid2014)
    m2014_2 = add_match("2014-06-13", "Group", t2014_mexico, t2014_netherlands, 1, 0, tid2014)
    m2014_3 = add_match("2014-06-14", "Group", t2014_brazil, t2014_netherlands, 1, 5, tid2014)
    m2014_4 = add_match("2014-06-15", "Group", t2014_germany, t2014_argentina, 4, 0, tid2014)
    m2014_5 = add_match("2014-06-16", "Group", t2014_argentina, t2014_germany, 2, 1, tid2014)
    m2014_6 = add_match("2014-06-17", "Round of 16", t2014_brazil, t2014_chile, 1, 1, tid2014)
    m2014_7 = add_match("2014-06-18", "Round of 16", t2014_colombia, t2014_uruguay, 2, 0, tid2014)
    m2014_8 = add_match("2014-07-08", "Semi-final", t2014_germany, t2014_brazil, 7, 1, tid2014)
    m2014_9 = add_match("2014-07-09", "Semi-final", t2014_argentina, t2014_netherlands, 0, 0, tid2014)
    m2014_10 = add_match("2014-07-13", "Final", t2014_germany, t2014_argentina, 1, 0, tid2014)


    # 2018 Russia tournament matches
    m2018_1 = add_match("2018-06-14", "Group", t2018_russia, t2018_spain, 5, 0, tid2018)
    m2018_2 = add_match("2018-06-15", "Group", t2018_france, t2018_uruguay, 0, 1, tid2018)
    m2018_3 = add_match("2018-06-16", "Group", t2018_portugal, t2018_spain, 3, 3, tid2018)
    m2018_4 = add_match("2018-06-17", "Group", t2018_france, t2018_belgium, 2, 1, tid2018)
    m2018_5 = add_match("2018-06-18", "Group", t2018_france, t2018_brazil, 1, 1, tid2018)
    m2018_6 = add_match("2018-06-19", "Group", t2018_brazil, t2018_russia, 1, 1, tid2018)
    m2018_7 = add_match("2018-06-20", "Round of 16", t2018_france, t2018_russia, 4, 3, tid2018)
    m2018_8 = add_match("2018-06-21", "Round of 16", t2018_uruguay, t2018_portugal, 2, 1, tid2018)
    m2018_9 = add_match("2018-07-14", "Semi-final", t2018_france, t2018_belgium, 1, 0, tid2018)
    m2018_10 = add_match("2018-07-15", "Final", t2018_france, t2018_croatia, 4, 2, tid2018)


        # 2022 Qatar tournament matches
    m2022_1 = add_match("2022-11-20", "Group", t2022_netherlands, t2022_england, 0, 2, tid2022)
    m2022_2 = add_match("2022-11-21", "Group", t2022_england, t2022_portugal, 6, 2, tid2022)
    m2022_3 = add_match("2022-11-22", "Group", t2022_brazil, t2022_netherlands, 0, 2, tid2022)
    m2022_4 = add_match("2022-11-23", "Group", t2022_spain, t2022_netherlands, 1, 1, tid2022)
    m2022_5 = add_match("2022-11-24", "Group", t2022_argentina, t2022_germany, 1, 2, tid2022)
    m2022_6 = add_match("2022-11-25", "Group", t2022_croatia, t2022_argentina, 0, 0, tid2022)
    m2022_7 = add_match("2022-12-03", "Round of 16", t2022_argentina, t2022_portugal, 2, 1, tid2022)
    m2022_8 = add_match("2022-12-04", "Round of 16", t2022_france, t2022_croatia, 3, 1, tid2022)
    m2022_9 = add_match("2022-12-17", "Semi-final", t2022_argentina, t2022_croatia, 3, 0, tid2022)
    m2022_10 = add_match("2022-12-18", "Final", t2022_argentina, t2022_france, 3, 3, tid2022)



    # -----------------------------
    # --- Key Events --------------
    # -----------------------------
    add_event(m2010_matches[0], p2010_players[0], 54, "Goal")
    add_event(m2010_matches[1], p2010_players[9], 77, "Goal")
    add_event(m2010_matches[2], p2010_players[17], 23, "Goal")
    add_event(m2010_matches[3], p2010_players[19], 45, "Goal")
    add_event(m2010_matches[4], p2010_players[25], 12, "Save")
    add_event(m2010_matches[5], p2010_players[0], 88, "Goal")
    add_event(m2010_matches[6], p2010_players[8], 60, "Goal")
    add_event(m2010_matches[7], p2010_players[0], 116, "Goal")
    add_event(m2010_matches[8], p2010_players[4], 55, "Goal")
    add_event(m2010_matches[9], p2010_players[0], 116, "Goal")

        # -----------------------------
    # --- Key Events 2014 ---------
    # -----------------------------
    add_event(m2014_1, p2014_players[0], 29, "Goal")    # Mario Götze
    add_event(m2014_1, p2014_players[7], 45, "Goal")    # Lionel Messi
    add_event(m2014_2, p2014_players[13], 60, "Save")   # Neymar
    add_event(m2014_3, p2014_players[18], 12, "Goal")   # Robin van Persie
    add_event(m2014_4, p2014_players[2], 75, "Assist")  # Toni Kroos
    add_event(m2014_5, p2014_players[8], 88, "Goal")    # Sergio Agüero
    add_event(m2014_6, p2014_players[21], 34, "Goal")   # Arjen Robben

    # -----------------------------
    # --- Key Events 2018 ---------
    # -----------------------------
    add_event(m2018_1, p2018_players[0], 18, "Goal")     # Kylian Mbappé
    add_event(m2018_1, p2018_players[7], 28, "Assist")   # Luka Modric
    add_event(m2018_2, p2018_players[12], 35, "Goal")    # Eden Hazard
    add_event(m2018_3, p2018_players[16], 42, "Goal")    # Harry Kane
    add_event(m2018_4, p2018_players[20], 50, "Assist")  # Neymar
    add_event(m2018_5, p2018_players[3], 68, "Goal")     # Antoine Griezmann
    add_event(m2018_6, p2018_players[1], 90, "Save")     # Hugo Lloris

    # -----------------------------
    # --- Key Events 2022 ---------
    # -----------------------------
    add_event(m2022_1, p2022_players[0], 23, "Goal")     # Lionel Messi
    add_event(m2022_1, p2022_players[7], 45, "Goal")     # Kylian Mbappé
    add_event(m2022_2, p2022_players[10], 60, "Assist")  # Enzo Fernández
    add_event(m2022_3, p2022_players[14], 70, "Goal")    # Antoine Griezmann
    add_event(m2022_4, p2022_players[20], 80, "Goal")    # Luka Modric
    add_event(m2022_5, p2022_players[17], 88, "Save")    # Hugo Lloris
    add_event(m2022_6, p2022_players[3], 115, "Goal")    # Emiliano Martínez



    # start GUI here (menu bar + view/add forms)
    # Main Tournaments Table in root window
    tournament_frame = tk.Frame(root)
    tournament_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree = ttk.Treeview(tournament_frame, columns=("ID", "Year", "Host", "Winner", "RunnerUp"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Year", text="Year")
    tree.heading("Host", text="Host Country")
    tree.heading("Winner", text="Winner")
    tree.heading("RunnerUp", text="Runner-up")
    tree.pack(fill=tk.BOTH, expand=True)

    # Buttons for edit/delete
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill=tk.X)
    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        data = view_tournaments()
        for t in data:
            tree.insert("", "end", values=t)

    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a tournament to edit")
            return
        tid = tree.item(selected[0])['values'][0]
        year = simpledialog.askinteger("Edit", "Year:", initialvalue=tree.item(selected[0])['values'][1])
        host = simpledialog.askstring("Edit", "Host Country:", initialvalue=tree.item(selected[0])['values'][2])
        winner = simpledialog.askstring("Edit", "Winner:", initialvalue=tree.item(selected[0])['values'][3])
        runner_up = simpledialog.askstring("Edit", "Runner-up:", initialvalue=tree.item(selected[0])['values'][4])
        edit_tournament(tid, year, host, winner, runner_up)
        refresh()

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a tournament to delete")
            return
        tid = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this tournament?"):
            delete_tournament(tid)
            refresh()

    tk.Button(btn_frame, text="Edit Selected", command=edit_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(btn_frame, text="Refresh", command=refresh).pack(side=tk.LEFT, padx=5, pady=5)

    refresh()  # populate table on startup

    # Menu Bar
    menu_bar = tk.Menu(root)

    # Tournament Menu
    tournament_menu = tk.Menu(menu_bar, tearoff=0)
    tournament_menu.add_command(label="Add Tournament", command=add_tournament_form)
    tournament_menu.add_command(label="View/Edit Tournaments", command=view_tournaments_table)
    menu_bar.add_cascade(label="Tournaments", menu=tournament_menu)

    # Teams Menu
    team_menu = tk.Menu(menu_bar, tearoff=0)
    team_menu.add_command(label="Add Team", command=add_team_form)
    team_menu.add_command(label="View/Edit Teams", command=view_teams_table)
    menu_bar.add_cascade(label="Teams", menu=team_menu)

    # Matches Menu
    match_menu = tk.Menu(menu_bar, tearoff=0)
    match_menu.add_command(label="Add Match", command=add_match_form)
    match_menu.add_command(label="View/Edit Matches", command=view_matches_table)
    menu_bar.add_cascade(label="Matches", menu=match_menu)

    # Players Menu
    player_menu = tk.Menu(menu_bar, tearoff=0)
    player_menu.add_command(label="Add Player", command=add_player_form)
    player_menu.add_command(label="View/Edit Players", command=view_players_table)
    menu_bar.add_cascade(label="Players", menu=player_menu)

    # Events Menu
    event_menu = tk.Menu(menu_bar, tearoff=0)
    event_menu.add_command(label="Add Event", command=add_event_form)
    event_menu.add_command(label="View/Edit Events", command=view_events_table)
    menu_bar.add_cascade(label="Events", menu=event_menu)

    
    # Analysis Menu
    analysis_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Analysis", menu=analysis_menu)
    analysis_menu.add_command(label="Leaderboard", command=leaderboard_form)
    analysis_menu.add_command(label="Top Players", command=top_players_form)
    analysis_menu.add_command(label="Match Key Events", command=match_events_form)
    analysis_menu.add_command(label="Tournament Trends", command=tournament_trends_form)

    # Exit
    def on_close():
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            root.destroy()
    menu_bar.add_command(label="Exit", command=root.quit)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.config(menu=menu_bar)
    root.mainloop()

