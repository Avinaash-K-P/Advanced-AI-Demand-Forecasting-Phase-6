import { Link, useNavigate } from "react-router-dom";
import { useState,useEffect } from "react";
import NotificationDropdown from "./NotificationDropDown";
import React from "react";
import {
  FaUserShield,
  FaUser,
  FaTachometerAlt,
  FaChartLine,
  FaUsersCog,
  FaClipboardList,
  FaFlask,
  FaFolderOpen,
  FaUserFriends,
  FaUpload,
  FaBrain,
  FaDownload,
  FaUserCircle,
  FaCog,
  FaSignOutAlt,
  FaBuilding,
  FaProjectDiagram,
  FaRobot,
  FaEdit,
  FaShieldAlt
} from "react-icons/fa";
import { getThemeStyles } from "./ThemeStyles";
import {toast} from "react-toastify";


function Layout({ children }) {

  const navigate = useNavigate();

  const username = localStorage.getItem("username"); // To display username in the dashboard

  const role = localStorage.getItem("role");

  const [showMenu,setShowMenu] = useState(false);

  const handleLogout = () => {

    localStorage.removeItem("token");

    navigate("/");
  };

  const [darkMode, setDarkMode] = useState(false);
  
  const styles = getThemeStyles(darkMode);

  const toggleTheme = () => {

    if(darkMode){

        document.documentElement
            .classList.remove("dark");

        localStorage.setItem(
            "theme",
            "light"
        );

    } else {

        document.documentElement
            .classList.add("dark");

        localStorage.setItem(
            "theme",
            "dark"
        );
    }

    setDarkMode(!darkMode);
};

  useEffect(() => {

  const token = localStorage.getItem("token");

  if (!token) {

    navigate("/");
    toast.error("Please log in to access the dashboard.");
  }

  }, []);


  useEffect(() => {

    const savedTheme =
        localStorage.getItem("theme");

    if(savedTheme === "dark"){

        document.documentElement
            .classList.add("dark");

        setDarkMode(true);
    }

}, []);

  return (

   <div
    className={`
    min-h-screen
    flex
    transition-all
    duration-300
    
     ${styles.layout}
    `}
    >

      {/* Sidebar */}
   
   <div className={`   

    ${styles.navBar}
    fixed
    top-0
    left-0
    h-screen
    w-56

    overflow-y-auto
    p-6

    hidden
    md:block

    shadow-2xl
    transition-all
    duration-300
    text-left

   `}
    >

      {(role === "super_admin" || role === "organization_admin") && (

        <div className="flex items-center gap-3 mb-10">
          <FaUserShield className="text-blue-400 text-2xl" />
          <p className="text-xl font-bold">
            Admin Panel
          </p>
        </div>

      )}

      {(role ==="manager" || role === "analyst" || role === "viewer") && (
      
        <div className="flex items-center gap-3 mb-10">
          <FaUser className="text-blue-400 text-2xl" />
          <p className="text-xl font-bold">
            User Panel
          </p>
        </div>

      )}

  <nav className="space-y-4">

    {/*ANALYTICS*/}

    <div className="mt-6 mb-2 px-4">
          <p className="
            text-base
            font-bold
            tracking-wide
            text-gray-300
          ">
            ANALYTICS
          </p>
        <div
        className="
          border-b
          border-gray-600
         "/>
        </div>

        <Link
          to="/dashboard"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
          >
            <FaTachometerAlt className="text-sm "/>
            <span className="text-sm text-sm truncate">Dashboard</span> 
        </Link>

        { /*ANALYST AND VIEWER RESTRICTED*/
          (role != "analyst" && role != "viewer") && (
            <>
  
        <Link
          to="/executive-dashboard"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaChartLine className="text-sm" />
          <span className="text-sm text-sm truncate">Executive</span>
        </Link>  

            </>
          )
        }

        { /*VIEWER RESTRICTED*/
          (role != "viewer") && (
            <>
        <Link
          to="/forecast-scenario"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaFlask className="text-sm" />
          <span className="text-sm text-sm truncate">Scenario</span>
        </Link>
         </>)
         }     

        {/* AI FORECASTING */}

      { /*MANAGER AND VIEWER RESTRICTED*/
          (role != "viewer" && role!= "manager") && (
            <>   

        <div className="mt-6 mb-2 px-4">
          <p className="
            text-base
            font-bold
            tracking-wide
            text-gray-300
          ">
            FORECASTING
          </p>
            <div
    className="
      border-b
      border-gray-600
    "
  />
        </div>


        <Link
          to="/upload"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaUpload className="text-sm" />
          <span className="text-sm text-sm truncate">Upload Data</span>
        </Link>
        


        <Link
          to="/forecast"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaBrain className="text-sm" />
          <span className="text-sm text-sm truncate">Forecast Data</span>
        </Link>

        </>)
        }

       {/* MANAGEMENT */}

       { /*MANAGER, ANALYST AND VIEWER RESTRICTED*/
          (role != "manager" && role !="analyst" && role!= "viewer") && (
            <>   

        <div className="mt-6 mb-2 px-4">
          <p className="
            text-base
            font-bold
            tracking-wide
            text-gray-300
          ">
            MANAGE
          </p>
            <div
    className="
      border-b
      border-gray-600
    "
  />
        </div>

        <Link
          to="/admin/management"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >

          <FaUsersCog className="text-sm" />
          <span className="text-sm text-sm truncate">Management</span>
        </Link>

              <Link
          to="/organization"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaBuilding className="text-sm" />
          <span className="text-sm text-sm truncate">Organization</span>
        </Link>  

        <Link
          to="/admin/activity-logs"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaClipboardList className="text-sm" />
          <span className="text-sm text-sm truncate">Activity Logs</span>
        </Link>
       </>
  )
}        

        {/* ENTERPRISE */}

       { /*ANALYST AND VIEWER RESTRICTED*/
          ( role !="analyst" && role!= "viewer") && (
            <>   

        <div className="mt-6 mb-2 px-4">
          <p className="
            text-base
            font-bold
            tracking-wide
            text-gray-300
          ">
            ENTERPRISE
          </p>
            <div
    className="
      border-b
      border-gray-600
    "
  />
        </div>

        <Link
          to="/workflow"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaProjectDiagram className="text-sm" />
          <span className="text-sm text-sm truncate">Workflow</span>
        </Link>

        <Link
          to="/planning"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaEdit className="text-sm" />
          <span className="text-sm text-sm truncate">Planning</span>
        </Link>

        <Link
          to="/governance"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaShieldAlt className="text-sm" />
          <span className="text-sm text-sm truncate">Governance</span>
        </Link>

      </>)
      }      

      {/*PROJECT*/}            

              <div className="mt-6 mb-2 px-4">
          <p className="
            text-base
            font-bold
            tracking-wide
            text-gray-300
          ">
            PROJECTS
          </p>
    <div
    className="
      border-b
      border-gray-600
    "
  />
        </div>      

        <Link
          to="/workspace"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaFolderOpen className="text-sm" />
          <span className="text-sm text-sm truncate">Workspace</span>
        </Link>

        <Link
          to="/collaboration"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaUserFriends className="text-sm" />
          <span className="text-sm text-sm truncate">Collaboration</span>
        </Link>

             <div className="mt-6 mb-2 px-4">
          <p className="
            text-base
            font-bold
            tracking-wide
            text-gray-300
          ">
            REPORTS
          </p>
    <div
    className="
      border-b
      border-gray-600
    "
  />
        </div>      

        <Link
          to="/download"
          className="
            flex items-center gap-3 px-4 py-2
            rounded-xl
            hover:bg-white/10
            hover:text-green-200
            transition
          "
        >
          <FaDownload className="text-sm" />
          <span className="text-sm text-sm truncate">Downloads</span>
        </Link>

     
  </nav>

</div>

{/*Top Bar*/}
<div className="
flex-1
flex
flex-col
ml-56
">

    <header
className={`
  
fixed
top-0
left-56
right-0

h-16
flex
items-center
justify-between

px-8

shadow-lg
z-50
      ${styles.navBar}
`}
>

        {/* Left */}

        <div
  className="
    flex items-center gap-2
    text-xl font-semibold
  "
>
  <FaRobot className="text-2xl text-blue-400" />

  <span >AI Demand Forecast</span>
</div>

        {/* Right */}

        <div
        className="
        flex
        items-center
        gap-6
        "
        >

           {/* Theme Toggle */}

  <button
    onClick={toggleTheme}
    className="
      flex items-center gap-2
      px-3 py-2
      rounded-xl
      hover:bg-white/10
      transition
    "
  >
    <span className="text-lg">
      {darkMode ? "☀" : "🌙"}
    </span>

    <span className="hidden md:inline">
      {darkMode ? "Light" : "Dark"}
    </span>
  </button>
              
            {/* Notification */}

          { <div className="       
          block px-4
             py-3
             rounded-xl
             hover:bg-white/10
             hover:text-green-200
             transition">
             <NotificationDropdown />
          </div> }

            {/* User Dropdown */}

            <div
            className="
            relative
            "
            >
    
    <div
onClick={() =>
setShowMenu(!showMenu)
}
className="
cursor-pointer
font-medium
"
>

Welcome {username} ▼

{
showMenu && (

<div
className={`
  ${styles.navBar}
  absolute
right-0
top-10

w-52

text-gray-700

rounded-2xl
shadow-2xl

border
border-gray-200

overflow-hidden

z-50`}

>

    {/* User Header */}

    <div
    className=" 
    px-4
    py-3

    bg-gradient-to-r
    from-emerald-50
    to-green-100

    border-b
    "
    >

        <p className="
        text-sm
        text-gray-500
        ">
            Signed In
        </p>

        <p className="
        font-semibold
        text-gray-800
        ">
            {username}
        </p>

    </div>

    {/* Profile */}

    <Link
        to="/profile"
        className="
        flex
        items-center
        gap-3

        px-4
        py-3

        hover:bg-green-50
        hover:text-green-700

        transition
        duration-200
        "
    >

        <FaUserCircle/>

        <span>
            Profile
        </span>

    </Link>

     <div className="border-t"></div>

    { (role !="analyst" && role!="viewer") &&
    (<>
            <Link
        to="/dashboard/settings"
        className="
        flex
        items-center
        gap-3

        px-4
        py-3

        hover:bg-green-50
        hover:text-green-700

        transition
        duration-200
        "
    >

        <FaCog/>

        <span>
            Widgets
        </span>

    </Link>  

      </>)
    }



    <div className="border-t"></div>

    {/* Logout */}

    <button

        onClick={handleLogout}

        className="
        w-full

        flex
        items-center
        gap-3

        px-4
        py-3

        text-left

        hover:bg-red-50
        hover:text-red-600

        transition
        duration-200
        "

    >

        <FaSignOutAlt/>

        <span>
            Logout
        </span>

    </button>

</div>

)
}


</div>


  </div>

        </div>

</header>


<main
className={`
  flex-1
  p-6
  pt-20
  overflow-y-auto

    ${styles.layout}
  `}
>

{children}

</main>
</div>
</div>
  
);
}

export default Layout;