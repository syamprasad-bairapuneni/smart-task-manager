import { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import { TrendingUp, Clock, Calendar, BarChart3 } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import toast from 'react-hot-toast';

const COLORS = ['#0ea5e9', '#a855f7', '#10b981', '#f59e0b', '#ef4444'];

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [weeklyData, setWeeklyData] = useState([]);
  const [productiveTime, setProductiveTime] = useState(null);
  const [completionTime, setCompletionTime] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const [statsRes, weeklyRes, productiveRes, completionRes] = await Promise.all([
        analyticsAPI.getStats(),
        analyticsAPI.getWeekly(),
        analyticsAPI.getProductiveTime(),
        analyticsAPI.getCompletionTime(),
      ]);

      setStats(statsRes.data.stats);
      setWeeklyData(weeklyRes.data.weekly_data || []);
      setProductiveTime(productiveRes.data.productive_time);
      setCompletionTime(completionRes.data.completion_time);
    } catch (error) {
      toast.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600 dark:text-gray-400">Loading analytics...</p>
      </div>
    );
  }

  const chartData = weeklyData.map((day) => ({
    date: new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' }),
    Completed: day.completed,
    Pending: day.pending,
    Total: day.total,
  }));

  const dayDistribution = productiveTime?.day_distribution ? Object.entries(productiveTime.day_distribution).map(([day, count]) => ({
    day,
    count,
  })) : [];

  const hourDistribution = productiveTime?.hour_distribution ? Object.entries(productiveTime.hour_distribution).map(([hour, count]) => ({
    hour: `${hour}:00`,
    count,
  })) : [];

  const priorityData = stats?.priority_counts ? Object.entries(stats.priority_counts).map(([priority, count]) => ({
    name: priority,
    value: count,
  })) : [];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Analytics</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">Deep insights into your productivity patterns</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-primary-100 dark:bg-primary-900 rounded-lg">
              <TrendingUp className="text-primary-600 dark:text-primary-400" size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Completion Rate</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {stats?.completion_rate?.toFixed(1) || 0}%
              </p>
            </div>
          </div>
        </div>

        {productiveTime?.most_productive_day && (
          <div className="card">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-accent-100 dark:bg-accent-900 rounded-lg">
                <Calendar className="text-accent-600 dark:text-accent-400" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Most Productive Day</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {productiveTime.most_productive_day}
                </p>
              </div>
            </div>
          </div>
        )}

        {completionTime && (
          <div className="card">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                <Clock className="text-green-600 dark:text-green-400" size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Avg. Completion Time</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {completionTime.average_hours?.toFixed(1) || 0}h
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Weekly Trends */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
            <BarChart3 size={20} />
            <span>Weekly Trends</span>
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="Completed" stroke="#10b981" strokeWidth={2} />
              <Line type="monotone" dataKey="Pending" stroke="#f59e0b" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Priority Distribution */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Priority Distribution</h2>
          {priorityData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={priorityData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {priorityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[300px] text-gray-500">
              No priority data available
            </div>
          )}
        </div>

        {/* Day Distribution */}
        {dayDistribution.length > 0 && (
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Productivity by Day</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={dayDistribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#0ea5e9" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Hour Distribution */}
        {hourDistribution.length > 0 && (
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Productivity by Hour</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={hourDistribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#a855f7" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Insights */}
      {productiveTime && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Productivity Insights</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {productiveTime.most_productive_day && (
              <div className="p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Most Productive Day</p>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">
                  {productiveTime.most_productive_day}
                </p>
              </div>
            )}
            {productiveTime.most_productive_hour !== undefined && (
              <div className="p-4 bg-accent-50 dark:bg-accent-900/20 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Most Productive Hour</p>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">
                  {productiveTime.most_productive_hour}:00
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

