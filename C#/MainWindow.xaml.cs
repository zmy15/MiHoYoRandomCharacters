using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;
using System.Windows.Threading;
using Newtonsoft.Json;

namespace 米哈游角色随机工具;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    private readonly Random random = new(); 
    private readonly DispatcherTimer starRailTimer = new();
    private readonly DispatcherTimer genshinTimer = new();
    private bool isRolling = false;
    private StarRailData starRailData = new();
    private GenshinData genshinData = new();
    private readonly string StarRailFile = "StarRail.json";
    private readonly string GenshinFile = "Genshin.json";
    
    public MainWindow()
    {
        InitializeComponent();
        var exePath = @"download.exe";
        RunExternalProgram(exePath);
        starRailTimer.Interval = TimeSpan.FromMilliseconds(50);
        starRailTimer.Tick += StarRailTimerTick;
        genshinTimer.Interval = TimeSpan.FromMilliseconds(50);
        genshinTimer.Tick += GenshinTimerTick;
    }
    private void LoadStarRailFile()
    {
        try
        {
            string jsonContent = File.ReadAllText(StarRailFile);
            starRailData.Characters = JsonConvert.DeserializeObject<Dictionary<string, StarRailCharacter>>(jsonContent);
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            throw;
        }
    }
    private void LoadGenshinFile()
    {
        try
        {
            string jsonContent = File.ReadAllText(GenshinFile);
            genshinData.Characters = JsonConvert.DeserializeObject<Dictionary<string, GenshinCharacter>>(jsonContent);
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            throw;
        }
    }
    private void StarRailTimerTick(object sender, EventArgs e)
    {
        LoadStarRailFile();
        List<string> charactersname = new List<string>();
        charactersname = starRailData.Characters.Values
            .Select(character => character.Name)
            .ToList();
        string randomCharacter = charactersname[random.Next(charactersname.Count)];
        var imagePath = "\\StarRail_Image\\"+ randomCharacter + ".png";
        LoadImage(StarRailImage,imagePath);
        StarRailName.Text = randomCharacter;
    }
    private void GenshinTimerTick(object sender, EventArgs e)
    {
        LoadGenshinFile();
        List<string> charactersname = new List<string>();
        charactersname = genshinData.Characters.Values
            .Select(character => character.Name)
            .ToList();
        string randomCharacter = charactersname[random.Next(charactersname.Count)];
        var imagePath = "\\Genshin_Image\\"+ randomCharacter + ".png";
        LoadImage(GenshinImage,imagePath);
        GenshinName.Text = randomCharacter;
    }
    private void StartRandomStarRail(object sender, RoutedEventArgs e)
    {
        starRailTimer.Start();
        isRolling = true;
    }
    private void StopRandomStarRail(object sender, RoutedEventArgs e)
    {
        starRailTimer.Stop();
        isRolling = false;
    }
    private void StartRandomGenshin(object sender, RoutedEventArgs e)
    {
        genshinTimer.Start();
        isRolling = true;
    }
    private void StopRandomGenshin(object sender, RoutedEventArgs e)
    {
        genshinTimer.Stop();
        isRolling = false;
    }
    private static void RunExternalProgram(string exePath)
    {
        ProcessStartInfo startInfo = new ProcessStartInfo
        {
            FileName = exePath, // 要运行的.exe文件路径
            UseShellExecute = false, // 是否使用操作系统外壳启动
            RedirectStandardOutput = false, 
            RedirectStandardError = false, 
            CreateNoWindow = false
        };

        using (Process process = new Process { StartInfo = startInfo })
        {
            try
            {
                process.Start();
                process.WaitForExit(); // 等待进程结束
            }
            catch (Exception ex)
            {
                Console.WriteLine("无法运行程序: " + ex.Message);
            }
        }
    }
    private void LoadImage(Image targetImage,string imagePath)
    {
        var currentDirectory = AppDomain.CurrentDomain.BaseDirectory;
        imagePath = currentDirectory + imagePath;
        BitmapImage bitmap = new();
        bitmap.BeginInit();
        bitmap.UriSource = new Uri(imagePath, UriKind.Absolute);
        bitmap.EndInit();
        targetImage.Source = bitmap;
    }
}

public class GenshinData
{
    public Dictionary<string, GenshinCharacter> Characters { get; set; }
}
public class GenshinCharacter
{
    public string Id { get; set; }
    public int Rank { get; set; }
    public string Name { get; set; }
    public string Element { get; set; }
    public string WeaponType { get; set; }
    public string Region { get; set; }
    public string SpecialProp { get; set; }
    public string BodyType { get; set; }
    public string Icon { get; set; }
    public List<int> Birthday { get; set; }
    public long Release { get; set; }
    public string Route { get; set; }
}

public class StarRailData
{
    public Dictionary<string, StarRailCharacter> Characters { get; set; }
}
public class StarRailCharacter
{
    public string Id { get; set; }
    public string Name { get; set; }
    public string Tag { get; set; }
    public int Rarity { get; set; }
    public string Path { get; set; }
    public string Element { get; set; }
    public int MaxSp { get; set; }
    public List<string> Ranks { get; set; }
    public List<string> Skills { get; set; }
    public List<string> SkillTrees { get; set; }
    public string Icon { get; set; }
    public string Preview { get; set; }
    public string Portrait { get; set; }
    public List<string> GuideOverview { get; set; }
}
