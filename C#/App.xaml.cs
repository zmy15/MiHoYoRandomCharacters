using System.Configuration;
using System.Data;
using System.Windows;

namespace 米哈游角色随机工具;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : Application
{
    public App()
    {
        this.DispatcherUnhandledException += App_DispatcherUnhandledException;
    }

    private void App_DispatcherUnhandledException(object sender, System.Windows.Threading.DispatcherUnhandledExceptionEventArgs e)
    {
        // 显示错误窗口
        MessageBox.Show($"发生未处理的异常：{e.Exception.Message}", "错误", MessageBoxButton.OK, MessageBoxImage.Error);

        // 阻止应用程序崩溃
        e.Handled = true;
    }
}